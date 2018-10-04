"""
Collections of CAN messages used for communication while calibrating E-Storage BTE higher FW v7.

Message basics: The data on CAN bus are sorted by INTEL byte-order, means least-significant bytes at least-significant
message byte order.
E.g. \x00\x00\x20\x03 represents 0x0320

The data is often converted to IEEE float what is a special kind of coding integer values.
Convertion described: https://stackoverflow.com/questions/24289180/how-to-convert-a-hex-string-into-an-unpacked-ieee-754-format-number
Converter: https://www.h-schmidt.net/FloatConverter/IEEE754de.html
"""

from can import Message

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
