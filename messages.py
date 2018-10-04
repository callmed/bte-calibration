"""
Collections of CAN messages used for communication while calibrating E-Storage BTE higher FW v7.

Message basics: The data on CAN bus are sorted by INTEL byte-order, means least-significant bytes at least-significant
message byte order.
E.g. \x00\x00\x20\x03 represents 0x0320

References:
The data is often converted to IEEE float what is a special kind of coding integer values.
Convertion described: https://stackoverflow.com/questions/24289180/how-to-convert-a-hex-string-into-an-unpacked-ieee-754-format-number
Converter: https://www.h-schmidt.net/FloatConverter/IEEE754de.html
STRUCT:
https://docs.python.org/3.6/library/struct.html
https://pymotw.com/2/struct/

"""


import binascii
import struct
from can import Message


SET_SLOPE_U_I = {"msg_id": 0x144,
                 "msg_fmt": "<ff",
                 "dlc": 8,
                 "slope_voltage": {"byte_size":4,
                                   "unit":"V",
                                   "factor:1},
                 "slope_current": {"byte_size":4,
                                   "unit":"A",
                                   "factor":1}
                }
                              

def load_set_slope_u_i(slope_voltage,slope_current):
  """Create CAN message object with data loaded.""" 
  payload = None
  msgfmt = SET_SLOPE_U_I["msg_fmt"]
  msgid = SET_SLOPE_U_I["msg_id"]
                 
  payload = struct.pack(msgfmt, slope_voltage, slope_current)
  #logger.debug("Message payload: ", binascii.hexlify(payload))
  return Message(arbitration_id=msgid,data=payload,extended_id=False)


def unload_set_slope_u_i(msg):
  """Return CAN message data from message object."""
  msgfmt = SET_SLOPE_U_I["msg_fmt"]
  voltage, current = struct.unpack(msgfmt, msg.data)
  return (voltage, current)
                              

                              
                              #
                              #   O B S O L E T E
                              #
                              
#TODO: Wrong data load in messages. Read description text about byte order and data conversion
msgSET_SLOPE_UI = Message(arbitration_id=324, extended_id=False, data=bytearray(b'\x00\x00\x00\xC8\x00\x00\x00\xC8'))
msgSET_PWR_SLOPE = Message(arbitration_id=340, extended_id=False, data=bytearray(b'\x00\x00\x00\x00\x00\x00\x00\xC8'))
msgSET_OP_LIM_U = Message(arbitration_id=336, extended_id=False, data=bytearray(b'\x00\x00\x00\x00\x00\x00\x03\x20'))
msgSET_OP_LIM_I = Message(arbitration_id=352, extended_id=False, data=bytearray(b'\x00\x00\x02\x58\x00\x00\x02\x58'))
msgSET_OP_LIM_PWR = Message(arbitration_id=368, extended_id=False, data=bytearray(b'\x00\x00\x01\xF4\x00\x00\x01\xF4'))


macroInitBTE = [msgSET_SLOPE_UI,
                msgSET_PWR_SLOPE,
                msgSET_OP_LIM_U,
                msgSET_OP_LIM_I,
                msgSET_OP_LIM_PWR
                ]
