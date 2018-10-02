"""
Collection of CAN messages from TAS to ESTORAGE mainly used during calibration.

"""

from canlib import canlib, Frame


def hexStringToInt(string):
	return int(string, 16)


def hexToIn(value):
	return int(value)


def intToHex(value):
	return hex(value)

# SET_UI_SLOPE
msg_set_ui_slope = Frame(id_=int(0x144), data=[,])


