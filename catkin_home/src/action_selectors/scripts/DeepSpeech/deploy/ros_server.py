"""Server-end for the ASR ROS requests."""
import time
import random
from os import path
import sys
import numpy as np
import argparse
import functools
# TODO: Check GPU Implementation.
import paddle.fluid as fluid
import rospkg
# TODO: Analyze why inside the DeepSpeech dir, everything can be imported
# directly without the package. Maybe is because the _init_paths.py and/or
# the `absolute_import`.
from DeepSpeech.deploy import _init_paths
from data_utils.data import DataGenerator
from model_utils.model import DeepSpeech2Model
from data_utils.utility import read_manifest
from utils.utility import add_arguments, print_arguments


NUM_CONV_LAYERS = 2
NUM_RNN_LAYERS = 3
RNN_LAYER_SIZE = 1024

USE_GRU = True
SHARE_RNN_WEIGHTS = False

SPECGRAM_TYPE = 'linear'


parser = argparse.ArgumentParser(description=__doc__)
add_arg = functools.partial(add_arguments, argparser=parser)

add_arg('beam_size',        int,    500,    "Beam search width.")
add_arg('alpha',            float,  2.5,   "Coef of LM for beam search.")
add_arg('beta',             float,  0.3,   "Coef of WC for beam search.")
add_arg('cutoff_prob',      float,  1.0,    "Cutoff probability for pruning.")
add_arg('cutoff_top_n',     int,    40,     "Cutoff number for pruning.")

add_arg('use_gpu',          bool,   False,   "Use GPU or not.")

rp = rospkg.RosPack()

deepspeech_home_path = path.join(rp.get_path("action_selectors"), "scripts", "DeepSpeech")
add_arg('warmup_manifest',  str,
        path.join(deepspeech_home_path, 'data/librispeech/manifest.test-clean'),
        "Filepath of manifest to warm up.")
add_arg('mean_std_path',    str,
        path.join(deepspeech_home_path, 'models/baidu_en8k/mean_std.npz'),
        "Filepath of normalizer's mean & std.")
add_arg('vocab_path',       str,
        path.join(deepspeech_home_path, 'models/baidu_en8k/vocab.txt'),
        "Filepath of vocabulary.")
add_arg('model_path',       str,
        path.join(deepspeech_home_path, 'models/baidu_en8k/'),
        "If None, the training starts from scratch, "
        "otherwise, it resumes from the pre-trained model.")
add_arg('lang_model_path',  str,
        path.join(deepspeech_home_path, 'models/lm/lm.binary'),
        "Filepath for language model.")
add_arg('decoding_method',  str,
        'ctc_beam_search',
        "Decoding method. Options: ctc_beam_search, ctc_greedy",
        choices = ['ctc_beam_search', 'ctc_greedy'])

args, unknown = parser.parse_known_args()


class ASRServer:
    def __init__(self, num_processes_beam_search=1):
        self.num_processes_beam_search = num_processes_beam_search
        print_arguments(args)
        
        if args.use_gpu:
            self.place = fluid.CUDAPlace(0)
        else:
            self.place = fluid.CPUPlace()
        
        self._start_server()


    def file_speech_to_text(self, filename):
        features = self.data_generator.process_utterance(filename, "")

        return self._predict_with_features(features)


    def bytes_speech_to_text(self, bytes):
        features = self.data_generator.process_utterance_from_bytes(
            bytes, "", 
            samplerate=48000, channels=1, format='RAW', 
            subtype='PCM_16', endian=['FILE', 'LITTLE', 'BIG', 'CPU'][1])

        return self._predict_with_features(features)

    def _process_features(self, feature):
        audio_len = feature[0].shape[1]
        mask_shape0 = (feature[0].shape[0] - 1) // 2 + 1
        mask_shape1 = (feature[0].shape[1] - 1) // 3 + 1
        mask_max_len = (audio_len - 1) // 3 + 1
        mask_ones = np.ones((mask_shape0, mask_shape1))
        mask_zeros = np.zeros((mask_shape0, mask_max_len - mask_shape1))
        mask = np.repeat(
            np.reshape(
                np.concatenate((mask_ones, mask_zeros), axis=1),
                (1, mask_shape0, mask_max_len)),
            32,
            axis=0)
        feature = (np.array([feature[0]]).astype('float32'),
                   None,
                   np.array([audio_len]).astype('int64').reshape([-1,1]),
                   np.array([mask]).astype('float32'))
        return feature

    def _predict_with_features(self, features):
        features = self._process_features(features)
        probs_split = self.ds2_model.infer_batch_probs(
            infer_data=features,
            feeding_dict=self.data_generator.feeding)

        if args.decoding_method == "ctc_greedy":
            result_transcript = self.ds2_model.decode_batch_greedy(
                probs_split=probs_split,
                vocab_list=self.vocab_list)
        else:
            result_transcript = self.ds2_model.decode_batch_beam_search(
                probs_split=probs_split,
                beam_alpha=args.alpha,
                beam_beta=args.beta,
                beam_size=args.beam_size,
                cutoff_prob=args.cutoff_prob,
                cutoff_top_n=args.cutoff_top_n,
                vocab_list=self.vocab_list,
                num_processes=self.num_processes_beam_search)

        return result_transcript[0]


    def _start_server(self):
        self.data_generator = DataGenerator(
            vocab_filepath=args.vocab_path,
            mean_std_filepath=args.mean_std_path,
            augmentation_config='{}',
            specgram_type=SPECGRAM_TYPE,
            place = self.place,
            keep_transcription_text=True)

        self.ds2_model = DeepSpeech2Model(
            vocab_size=self.data_generator.vocab_size,
            num_conv_layers=NUM_CONV_LAYERS,
            num_rnn_layers=NUM_RNN_LAYERS,
            rnn_layer_size=RNN_LAYER_SIZE,
            use_gru=USE_GRU,
            init_from_pretrained_model=args.model_path,
            place = self.place,
            share_rnn_weights=SHARE_RNN_WEIGHTS)
        
        self.vocab_list = [chars for chars in self.data_generator.vocab_list]
        
        if args.decoding_method == "ctc_beam_search":
            self.ds2_model.init_ext_scorer(args.alpha, args.beta, args.lang_model_path,
                                    self.vocab_list)


        print('-----------------------------------------------------------')
        print('Warming up ...')
        self._warm_up_test(num_test_cases=3)
        print('-----------------------------------------------------------')


    def _warm_up_test(self, num_test_cases, random_seed=0):
        manifest = read_manifest(args.warmup_manifest)
        rng = random.Random(random_seed)
        samples = rng.sample(manifest, num_test_cases)


        for idx, sample in enumerate(samples):
            print("Warm-up Test Case %d: %s", idx, sample['audio_filepath'])

            start_time = time.time()
            transcript = self.file_speech_to_text(sample['audio_filepath'])
            finish_time = time.time()

            print("Response Time: %f, Transcript: %s" %
                (finish_time - start_time, transcript))


# Verify that the needed files are downloaded and ready to use.
error_and_exit = False

if not path.isfile(args.mean_std_path):
    print("ERROR[DeepSpeech]: The file for 'mean_std' seems to be missing.")
    print("It should be in " + args.mean_std_path)

    print("To download it go to " +
        "models/baidu_en8k and run download_model.sh .\n")

    error_and_exit = True

if not path.isfile(args.vocab_path):
    print("ERROR[DeepSpeech]: The file for 'vocabulary' seems to be missing.")
    print("It should be in " + args.vocab_path)

    print("To download it go to " +
        "models/baidu_en8k and run download_model.sh .\n")
    
    error_and_exit = True

if not path.isfile(args.warmup_manifest):
    print("ERROR[DeepSpeech]: The file for 'warmup_manifest' seems to be missing.")
    print("It should be in " + args.warmup_manifest)

    print("To download it executes the python script " +
        "DeepSpeech/data/librispeech/librispeech.py in the DeepSpeech folder in following way: " +
        "python3 -m data.librispeech.librispeech --full_download False --manifest_prefix \"data/librispeech/manifest\" " +
        "\n")
    
    error_and_exit = True

if not path.isfile(args.lang_model_path):
    print("ERROR[DeepSpeech]: The file for 'lang_model' seems to be missing.")
    print("It should be in " + args.lang_model_path)

    print("To download it go to " +
        "https://github.com/diegocardozo97/DeepSpeech/releases " +
        "and select the file called 'language_model-mozilla.zip', " +
        "extract it and inside is the needed file.\n")
    
    error_and_exit = True

if error_and_exit:
    sys.exit()
