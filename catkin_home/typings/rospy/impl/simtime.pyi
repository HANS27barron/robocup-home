"""
This type stub file was generated by pyright.
"""

"""Internal-use: Support for simulated clock."""
_ROSCLOCK = '/clock'
_USE_SIMTIME = '/use_sim_time'
_rostime_sub = None
_rosclock_sub = None
def init_simtime():
    """
    Initialize the ROS time system by connecting to the /time topic
    IFF the /use_sim_time parameter is set.
    """
    ...
