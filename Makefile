# ----------------------------------------------------------------------
#  Development Noetic
# ----------------------------------------------------------------------

#: Builds a Docker image from the current Dockerfile file
noetic.build:
	@docker build -t ros:noetic -f docker/noetic/Dockerfile .
noetic.speech.build:
	@docker build -t ros:noetic-speech -f docker/noetic/Dockerfile.speech .
noetic.navigation.build:
	@docker build -t ros:noetic-navigation -f docker/noetic/Dockerfile.navigation .

#: Create Docker container
noetic.create: 
	@docker run \
		-it -d \
		-v ${shell pwd}/catkin_home/src:/catkin_home/src \
		-v ${shell pwd}/catkin_home/typings:/catkin_home/typings \
		--network host \
		--name ros-noetic \
		ros:noetic
noetic.speech.create:
	@./docker/noetic/runSpeech.bash
noetic.navigation.create:
	@./docker/noetic/runNavigation.bash

#: Start the container in background
noetic.up:
	@docker start ros-noetic
noetic.speech.up:
	@docker start ros-noetic-speech
noetic.navigation.up:
	@docker start ros-noetic-navigation

#: Stop the container
noetic.down:
	@docker stop ros-noetic
noetic.speech.down:
	@docker stop ros-noetic-speech
noetic.navigation.down:
	@docker stop ros-noetic-navigation

#: Restarts the container
noetic.restart:
	@docker restart ros-noetic
noetic.speech.restart:
	@docker restart ros-noetic-speech
noetic.navigation.restart:
	@docker restart ros-noetic-navigation

#: Shows the logs of the ros-noetic service container
noetic.logs:
	@docker logs --tail 50 ros-noetic
noetic.speech.logs:
	@docker logs --tail 50 ros-noetic-speech
noetic.navigation.logs:
	@docker logs --tail 50 ros-noetic-navigation

#: Fires up a bash session inside the ros-noetic service container
noetic.shell:
	@docker exec -it ros-noetic bash
noetic.speech.shell:
	@docker exec -it ros-noetic-speech bash
noetic.navigation.shell:
	@docker exec -it ros-noetic-navigation bash

#: Remove ros-noetic container. 
noetic.remove: noetic.down
	@docker container rm ros-noetic
noetic.speech.remove: noetic.speech.down
	@docker container rm ros-noetic-speech
noetic.navigation.remove: noetic.navigation.down
	@docker container rm ros-noetic-navigation

# ----------------------------------------------------------------------
#  Development Melodic
# ----------------------------------------------------------------------

#: Builds a Docker image from the current Dockerfile file
melodic.build:
	@docker build -t ros:melodic -f docker/melodic/Dockerfile .
melodic.speech.build:
	@docker build -t ros:melodic-speech -f docker/melodic/Dockerfile.speech .
melodic.speech.gpu.build:
	@docker build -t ros:melodic-speech-gpu -f docker/melodic/Dockerfile.speech.gpu .
melodic.navigation.build:
	@docker build -t ros:melodic-navigation -f docker/melodic/Dockerfile.navigation .
melodic.navigation.gpu.build:
	@docker build -t ros:melodic-navigation-gpu -f docker/melodic/Dockerfile.navigation.gpu .

#: Create Docker container
melodic.create: 
	@docker run \
		-it -d \
		-v ${shell pwd}/catkin_home/src:/catkin_home/src \
		-v ${shell pwd}/catkin_home/typings:/catkin_home/typings \
		--network host \
		--name ros-melodic \
		ros:melodic
melodic.speech.create:
	@docker run \
		-it -d \
		--device /dev/snd:/dev/snd \
		-v ${shell pwd}/catkin_home/src:/catkin_home/src \
		-v /catkin_home/src/action_selectors/scripts/DeepSpeech/decoders/swig  \
		-v /catkin_home/src/action_selectors/scripts/DeepSpeech/data/librispeech  \
		-v ${shell pwd}/catkin_home/typings:/catkin_home/typings \
		--network host \
		--name ros-melodic-speech \
		ros:melodic-speech
melodic.speech.gpu.create:
	@docker run \
		-it -d \
		--gpus all \
		--device /dev/snd:/dev/snd \
		-v ${shell pwd}/catkin_home/src:/catkin_home/src \
		-v /catkin_home/src/action_selectors/scripts/DeepSpeech/decoders/swig  \
		-v /catkin_home/src/action_selectors/scripts/DeepSpeech/data/librispeech  \
		-v ${shell pwd}/catkin_home/typings:/catkin_home/typings \
		--network host \
		--name ros-melodic-speech-gpu \
		ros:melodic-speech-gpu
melodic.navigation.create:
	@./docker/melodic/runNavigation.bash
melodic.navigation.gpu.create:
	@./docker/melodic/runNavigationGpu.bash

#: Start the container in background
melodic.up:
	@docker start ros-melodic
melodic.speech.up:
	@docker start ros-melodic-speech
melodic.speech.gpu.up:
	@docker start ros-melodic-speech-gpu
melodic.navigation.up:
	@docker start ros-melodic-navigation
melodic.navigation.gpu.up:
	@docker start ros-melodic-navigation-gpu

#: Stop the container
melodic.down:
	@docker stop ros-melodic
melodic.speech.down:
	@docker stop ros-melodic-speech
melodic.speech.gpu.down:
	@docker stop ros-melodic-speech-gpu
melodic.navigation.down:
	@docker stop ros-melodic-navigation
melodic.navigation.gpu.down:
	@docker stop ros-melodic-navigation-gpu

#: Restarts the container
melodic.restart:
	@docker restart ros-melodic
melodic.speech.restart:
	@docker restart ros-melodic-speech
melodic.speech.gpu.restart:
	@docker restart ros-melodic-speech-gpu
melodic.navigation.restart:
	@docker restart ros-melodic-navigation
melodic.navigation.gpu.restart:
	@docker restart ros-melodic-navigation-gpu

#: Shows the logs of the ros-melodic service container
melodic.logs:
	@docker logs --tail 50 ros-melodic
melodic.speech.logs:
	@docker logs --tail 50 ros-melodic-speech
melodic.speech.gpu.logs:
	@docker logs --tail 50 ros-melodic-speech-gpu
melodic.navigation.logs:
	@docker logs --tail 50 ros-melodic-navigation
melodic.navigation.gpu.logs:
	@docker logs --tail 50 ros-melodic-navigation-gpu

#: Fires up a bash session inside the ros-melodic service container
melodic.shell:
	@docker exec -it ros-melodic bash
melodic.speech.shell:
	@docker exec -it ros-melodic-speech bash
melodic.speech.gpu.shell:
	@docker exec -it ros-melodic-speech-gpu bash
melodic.navigation.shell:
	@docker exec -it ros-melodic-navigation bash
melodic.navigation.gpu.shell:
	@docker exec -it ros-melodic-navigation-gpu bash

#: Remove ros-melodic container. 
melodic.remove: melodic.down
	@docker container rm ros-melodic
melodic.speech.remove: melodic.speech.down
	@docker container rm ros-melodic-speech
melodic.speech.gpu.remove: melodic.speech.gpu.down
	@docker container rm ros-melodic-speech-gpu
melodic.navigation.remove: melodic.navigation.down
	@docker container rm ros-melodic-navigation
melodic.navigation.gpu.remove: melodic.navigation.gpu.down
	@docker container rm ros-melodic-navigation-gpu

# ----------------------------------------------------------------------
#  General Docker
# ----------------------------------------------------------------------

#: Show a list of containers.
list:
	@docker container ls -a

#: Show a list of containers.
listUp:
	@docker ps
