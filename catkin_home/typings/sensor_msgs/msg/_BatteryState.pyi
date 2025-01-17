"""
This type stub file was generated by pyright.
"""

import sys
import genpy

"""autogenerated by genpy from sensor_msgs/BatteryState.msg. Do not edit."""
python3 = True if sys.hexversion > 50331648 else False
class BatteryState(genpy.Message):
  _md5sum = ...
  _type = ...
  _has_header = ...
  _full_text = ...
  POWER_SUPPLY_STATUS_UNKNOWN = ...
  POWER_SUPPLY_STATUS_CHARGING = ...
  POWER_SUPPLY_STATUS_DISCHARGING = ...
  POWER_SUPPLY_STATUS_NOT_CHARGING = ...
  POWER_SUPPLY_STATUS_FULL = ...
  POWER_SUPPLY_HEALTH_UNKNOWN = ...
  POWER_SUPPLY_HEALTH_GOOD = ...
  POWER_SUPPLY_HEALTH_OVERHEAT = ...
  POWER_SUPPLY_HEALTH_DEAD = ...
  POWER_SUPPLY_HEALTH_OVERVOLTAGE = ...
  POWER_SUPPLY_HEALTH_UNSPEC_FAILURE = ...
  POWER_SUPPLY_HEALTH_COLD = ...
  POWER_SUPPLY_HEALTH_WATCHDOG_TIMER_EXPIRE = ...
  POWER_SUPPLY_HEALTH_SAFETY_TIMER_EXPIRE = ...
  POWER_SUPPLY_TECHNOLOGY_UNKNOWN = ...
  POWER_SUPPLY_TECHNOLOGY_NIMH = ...
  POWER_SUPPLY_TECHNOLOGY_LION = ...
  POWER_SUPPLY_TECHNOLOGY_LIPO = ...
  POWER_SUPPLY_TECHNOLOGY_LIFE = ...
  POWER_SUPPLY_TECHNOLOGY_NICD = ...
  POWER_SUPPLY_TECHNOLOGY_LIMN = ...
  __slots__ = ...
  _slot_types = ...
  def __init__(self, *args, **kwds) -> None:
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.

    The available fields are:
       header,voltage,current,charge,capacity,design_capacity,percentage,power_supply_status,power_supply_health,power_supply_technology,present,cell_voltage,location,serial_number

    :param args: complete set of field values, in .msg order
    :param kwds: use keyword arguments corresponding to message field names
    to set specific fields.
    """
    ...
  
  def serialize(self, buff):
    """
    serialize message into buffer
    :param buff: buffer, ``StringIO``
    """
    ...
  
  def deserialize(self, str):
    """
    unpack serialized message in str into this message instance
    :param str: byte array of serialized message, ``str``
    """
    ...
  
  def serialize_numpy(self, buff, numpy):
    """
    serialize message with numpy array types into buffer
    :param buff: buffer, ``StringIO``
    :param numpy: numpy python module
    """
    ...
  
  def deserialize_numpy(self, str, numpy):
    """
    unpack serialized message in str into this message instance using numpy for array types
    :param str: byte array of serialized message, ``str``
    :param numpy: numpy python module
    """
    ...
  


_struct_I = genpy.struct_I
_struct_3I = None
_struct_6f4B = None
