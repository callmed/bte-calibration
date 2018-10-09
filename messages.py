#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#TODO:
#TODO:

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


import logging
import binascii
import struct
from can import Message
from main import logger



SET_SLOPE_U_I = {"msg_id": 0x144,
                 "msg_fmt": "<ff",
                 "dlc": 8,
                 "freq": 10,
                 "slope_voltage": {"byte_size":4,
                                   "unit":"V",
                                   "factor":1},
                 "slope_current": {"byte_size":4,
                                   "unit":"A",
                                   "factor":1}
                }


SET_SLOPE_PWR_FILTER = {"msg_id": 0x154,
                 "msg_fmt": "<fh",
                 "dlc": 6,
                 "freq": 10,
                 "slope_power": {"byte_size":4,
                                   "unit":"W",
                                   "factor":1},
                 "filter": {"byte_size":2,
                                   "unit":" ",
                                   "factor":1}
                }


SET_OP_LIM_U = {"msg_id": 0x150,
                 "msg_fmt": "<ff",
                 "dlc": 8,
                 "freq": 100,
                 "op_lim_u_mn": {"byte_size":4,
                                   "unit":"V",
                                   "factor":1},
                 "op_lim_u_mx": {"byte_size":4,
                                   "unit":"V",
                                   "factor":1}
                }


SET_OP_LIM_I = {"msg_id": 0x160,
                 "msg_fmt": "<ff",
                 "dlc": 8,
                 "freq": 100,
                 "op_lim_i_mn": {"byte_size":4,
                                   "unit":"A",
                                   "factor":1},
                 "op_lim_i_mx": {"byte_size":4,
                                   "unit":"A",
                                   "factor":1}
                }


SET_OP_LIM_PWR = {"msg_id": 0x170,
                 "msg_fmt": "<ff",
                 "dlc": 8,
                 "freq": 100,
                 "op_lim_p_mn": {"byte_size":4,
                                   "unit":"W",
                                   "factor":1},
                 "op_lim_p_mx": {"byte_size":4,
                                   "unit":"W",
                                   "factor":1}
                }


SET_PR_LIM_U = {"msg_id": 0x114,
                 "msg_fmt": "<ff",
                 "dlc": 8,
                 "freq": 10,
                 "op_lim_u_mn": {"byte_size":4,
                                   "unit":"V",
                                   "factor":1},
                 "op_lim_u_mx": {"byte_size":4,
                                   "unit":"V",
                                   "factor":1}
                }


SET_PR_LIM_I = {"msg_id": 0x124,
                 "msg_fmt": "<ff",
                 "dlc": 8,
                 "freq": 10,
                 "op_lim_i_mn": {"byte_size":4,
                                   "unit":"A",
                                   "factor":1},
                 "op_lim_i_mx": {"byte_size":4,
                                   "unit":"A",
                                   "factor":1}
                }


SET_PR_LIM_PWR = {"msg_id": 0x134,
                 "msg_fmt": "<ff",
                 "dlc": 8,
                 "freq": 10,
                 "op_lim_p_mn": {"byte_size":4,
                                   "unit":"W",
                                   "factor":1},
                 "op_lim_p_mx": {"byte_size":4,
                                   "unit":"W",
                                   "factor":1}
                }


CLEARANCE = {"msg_id": 0x720,
                 "msg_fmt": "<b",
                 "dlc": 1,
                 "freq": 10,
                 "clearance": {"byte_size":1,
                                   "unit":" ",
                                   "factor":1}
                }


SET_RST_STOP = {"msg_id": 0x21F,
                 "msg_fmt": "<b",
                 "dlc": 1,
                 "freq": 1,
                 "clearance": {"byte_size":1,
                                   "unit":" ",
                                   "factor":1}
                }


"""

        FUNCTION TO LOAD DATA INTO CAN MESSAGES

"""


def load_message(_id, fmt, extended_id=False, **kwargs):
    """Universal function to load data into a CAN message object.
    The data must be provided as kwargs to ensure propper message data logging in the future.
    TODO: Detailed error handling of struct, e.g. formatting errors
    """
    payload = None
    try:
        payload = struct.pack(fmt, *kwargs.values())
    except struct.error as e:
        print("Error in struct.pack", e)
    return Message(arbitration_id=_id, data=payload, extended_id=extended_id)


def load_clearance(clearance):
    """Create CAN message object with data loaded."""
    payload = None
    msgfmt = CLEARANCE["msg_fmt"]
    msgid = CLEARANCE["msg_id"]
    payload = struct.pack(msgfmt, clearance)
    logger.info("Clearance sent via CAN")
    return Message(arbitration_id=msgid,data=payload,extended_id=False)


def load_set_rst_stop(rst_stop):
    """Create CAN message object with data loaded."""
    payload = None
    msgfmt = SET_RST_STOP["msg_fmt"]
    msgid = SET_RST_STOP["msg_id"]
    payload = struct.pack(msgfmt, rst_stop)
    return Message(arbitration_id=msgid,data=payload,extended_id=False)


def load_set_slope_u_i(slope_voltage,slope_current):
  """Create CAN message object with data loaded.""" 
  payload = None
  msgfmt = SET_SLOPE_U_I["msg_fmt"]
  msgid = SET_SLOPE_U_I["msg_id"]
  payload = struct.pack(msgfmt, slope_voltage, slope_current)
  logger.debug("Message payload: ", binascii.hexlify(payload))
  return Message(arbitration_id=msgid,data=payload,extended_id=False)


def load_set_slope_pwr_filter(slope_power, filter):
    """Create CAN message object with data loaded."""
    payload = None
    msgfmt = SET_SLOPE_PWR_FILTER["msg_fmt"]
    msgid = SET_SLOPE_PWR_FILTER["msg_id"]
    payload = struct.pack(msgfmt, slope_power, filter)
    #logger.debug("Message payload: ", binascii.hexlify(payload))
    return Message(arbitration_id=msgid, data=payload, extended_id=False)


def load_set_op_lim_u(op_lim_u_mn, op_lim_u_mx):
    """Create CAN message object with data loaded."""
    payload = None
    msgfmt = SET_OP_LIM_U["msg_fmt"]
    msgid = SET_OP_LIM_U["msg_id"]
    payload = struct.pack(msgfmt, op_lim_u_mx, op_lim_u_mn)
    # logger.debug("Message payload: ", binascii.hexlify(payload))
    return Message(arbitration_id=msgid, data=payload, extended_id=False)


def load_set_op_lim_i(op_lim_i_mn, op_lim_i_mx):
    """Create CAN message object with data loaded."""
    payload = None
    msgfmt = SET_OP_LIM_I["msg_fmt"]
    msgid = SET_OP_LIM_I["msg_id"]
    payload = struct.pack(msgfmt, op_lim_i_mx, op_lim_i_mn)
    # logger.debug("Message payload: ", binascii.hexlify(payload))
    return Message(arbitration_id=msgid, data=payload, extended_id=False)


def load_set_op_lim_pwr(op_lim_pwr_mn, op_lim_pwr_mx):
    """Create CAN message object with data loaded."""
    payload = None
    msgfmt = SET_OP_LIM_PWR["msg_fmt"]
    msgid = SET_OP_LIM_PWR["msg_id"]
    payload = struct.pack(msgfmt, op_lim_pwr_mn, op_lim_pwr_mx)
    # logger.debug("Message payload: ", binascii.hexlify(payload))
    return Message(arbitration_id=msgid, data=payload, extended_id=False)


def load_set_pr_lim_u(pr_lim_u_mn, pr_lim_u_mx):
    """Create CAN message object with data loaded."""
    payload = None
    msgfmt = SET_PR_LIM_U["msg_fmt"]
    msgid = SET_PR_LIM_U["msg_id"]
    payload = struct.pack(msgfmt, pr_lim_u_mn, pr_lim_u_mx)
    # logger.debug("Message payload: ", binascii.hexlify(payload))
    return Message(arbitration_id=msgid, data=payload, extended_id=False)


def load_set_pr_lim_i(pr_lim_i_mn, pr_lim_i_mx):
    """Create CAN message object with data loaded."""
    payload = None
    msgfmt = SET_PR_LIM_I["msg_fmt"]
    msgid = SET_PR_LIM_I["msg_id"]
    payload = struct.pack(msgfmt, pr_lim_i_mn, pr_lim_i_mx)
    # logger.debug("Message payload: ", binascii.hexlify(payload))
    return Message(arbitration_id=msgid, data=payload, extended_id=False)


def load_set_pr_lim_pwr(pr_lim_pwr_mn, pr_lim_pwr_mx):
    """Create CAN message object with data loaded."""
    payload = None
    msgfmt = SET_PR_LIM_PWR["msg_fmt"]
    msgid = SET_PR_LIM_PWR["msg_id"]
    payload = struct.pack(msgfmt, pr_lim_pwr_mn, pr_lim_pwr_mx)
    # logger.debug("Message payload: ", binascii.hexlify(payload))
    return Message(arbitration_id=msgid, data=payload, extended_id=False)



"""

        FUNCTION TO UNLOAD DATA FROM CAN MESSAGES

"""


def unload_set_slope_u_i(msg):
  """Return CAN message data from message object."""
  msgfmt = SET_SLOPE_U_I["msg_fmt"]
  voltage, current = struct.unpack(msgfmt, msg.data)
  return (voltage, current)
