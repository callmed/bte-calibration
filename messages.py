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

import sys
import struct
import binascii
from can import Message, CanError
import logging


logger = logging.getLogger("calibration.protocol.messages")
logger.setLevel(logging.DEBUG)


"""

    C A N   M E S S A G E   D E S C R I P T I O N S 

"""

SET_SLOPE_U_I = {"msg_id": 0x144,
                 "msg_fmt": "<ff",
                 "msg_name": "SET_SLOPE_U_I",
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
                 "msg_name": "SET_SLOPE_PWR_FILTER",
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
                "msg_name": "SET_OP_LIM_U",
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
                "msg_name": "SET_OP_LIM_I",
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
                  "msg_name": "SET_OP_LIM_PWR",
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
                "msg_name": "SET_PR_LIM_U",
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
                "msg_name": "SET_PR_LIM_I",
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
                  "msg_name": "SET_PR_LIM_PWR",
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
             "msg_name": "CLEARANCE",
                 "dlc": 1,
                 "freq": 10,
                 "clearance": {"byte_size":1,
                                   "unit":" ",
                                   "factor":1}
                }


SET_RST_STOP = {"msg_id": 0x21F,
                 "msg_fmt": "<b",
                "msg_name": "SET_RST_STOP",
                 "dlc": 1,
                 "freq": 1,
                 "clearance": {"byte_size":1,
                                   "unit":" ",
                                   "factor":1}
                }


SET_REF_SWITCH_CTRL_RI = {"msg_id": 0xC1,
                 "msg_fmt": "<fbbh",
                  "msg_name": "SET_REF_SWITCH_CTRL_RI",
                 "dlc": 8,
                 "freq": 1000,
                 "set_ref": {"byte_size":4,
                                   "unit":" ",
                                   "factor":1},
                 "set_switch": {"byte_size":0,
                                   "unit":" ",
                                   "factor":1},
                 "set_ctrl": {"byte_size":0,
                                   "unit":" ",
                                   "factor":1},
                 "rst_q": {"byte_size":0,
                                   "unit":" ",
                                   "factor":1},
                 "rst_e": {"byte_size":0,
                                   "unit":" ",
                                   "factor":1},
                 "set_ri": {"byte_size":3,
                                   "unit":" ",
                                   "factor":1}
                }


"""

    F U N C T I O N S   T O   L O A D   D A T A   O N   C A N   M E S S A G E S 

"""

def load_message(msg_info, extended_flag=False, **kwargs):
    """ Universal function to load data based on message dictionary.

    :param msg_info: Dictionary containing details about the CAN message.
    :param extended_flag: Whether the message has an extended CAN id or not
    :param kwargs: List of data that are loaded to the CAN message. The order of data must relate tot he message format
    :return: CAN.Message object
    """
    message = None
    try:
        msg_id = msg_info["msg_id"]
        msg_name = msg_info["msg_name"]
        data_format = msg_info["msg_fmt"]

        payload = struct.pack(data_format, *kwargs.values())
        logger.debug("Payload: %s loaded to Message: %s", binascii.hexlify(payload), msg_name)

        message = Message(arbitration_id=msg_id, data=payload, extended_id=extended_flag)
    except struct.error:
        logger.error("Error occurred while packing data", exc_info=True)
        return None
    except KeyError:
        logger.error("Message information not complete, dictionary keyword missing", exc_info=True)
        return None
    except CanError:
        logger.error("CAN message object could not be created", exc_info=True)
    return message


def load_clearance(clearance):
    """Create CAN message object with data loaded."""
    payload = None
    msgfmt = CLEARANCE["msg_fmt"]
    msgid = CLEARANCE["msg_id"]
    payload = struct.pack(msgfmt, clearance)
    logger.debug("Data loaded to message")
    return Message(arbitration_id=msgid,data=payload,extended_id=False)


def load_set_rst_stop(rst_stop):
    """Create CAN message object with data loaded."""
    payload = None
    msgfmt = SET_RST_STOP["msg_fmt"]
    msgid = SET_RST_STOP["msg_id"]
    payload = struct.pack(msgfmt, rst_stop)
    logger.debug("Data loaded to message")
    return Message(arbitration_id=msgid,data=payload,extended_id=False)


def load_set_slope_u_i(slope_voltage,slope_current):
  """Create CAN message object with data loaded."""
  payload = None
  msgfmt = SET_SLOPE_U_I["msg_fmt"]
  msgid = SET_SLOPE_U_I["msg_id"]
  payload = struct.pack(msgfmt, slope_voltage, slope_current)
  #logger.debug("Message payload: ", binascii.hexlify(payload))
  logger.debug("Data loaded to message")
  return Message(arbitration_id=msgid,data=payload,extended_id=False)


def load_set_slope_pwr_filter(slope_power, filter=0):
    """Create CAN message object with data loaded."""
    payload = None
    msgfmt = SET_SLOPE_PWR_FILTER["msg_fmt"]
    msgid = SET_SLOPE_PWR_FILTER["msg_id"]
    payload = struct.pack(msgfmt, slope_power, filter)
    logger.debug("Payload: %s loaded to Message: %s", binascii.hexlify(payload), load_set_slope_pwr_filter.__name__)
    return Message(arbitration_id=msgid, data=payload, extended_id=False)


def load_set_op_lim_u(op_lim_u_mn, op_lim_u_mx):
    """Create CAN message object with data loaded."""
    payload = None
    msgfmt = SET_OP_LIM_U["msg_fmt"]
    msgid = SET_OP_LIM_U["msg_id"]
    payload = struct.pack(msgfmt, op_lim_u_mx, op_lim_u_mn)
    logger.debug("Message payload: ", binascii.hexlify(payload))
    return Message(arbitration_id=msgid, data=payload, extended_id=False)


def load_set_op_lim_i(op_lim_i_mn, op_lim_i_mx):
    """Create CAN message object with data loaded."""
    payload = None
    msgfmt = SET_OP_LIM_I["msg_fmt"]
    msgid = SET_OP_LIM_I["msg_id"]
    payload = struct.pack(msgfmt, op_lim_i_mx, op_lim_i_mn)
    logger.debug("Message payload: ", binascii.hexlify(payload))
    return Message(arbitration_id=msgid, data=payload, extended_id=False)


def load_set_op_lim_pwr(op_lim_pwr_mn, op_lim_pwr_mx):
    """Create CAN message object with data loaded."""
    payload = None
    msgfmt = SET_OP_LIM_PWR["msg_fmt"]
    msgid = SET_OP_LIM_PWR["msg_id"]
    payload = struct.pack(msgfmt, op_lim_pwr_mn, op_lim_pwr_mx)
    logger.debug("Message payload: ", binascii.hexlify(payload))
    return Message(arbitration_id=msgid, data=payload, extended_id=False)


def load_set_pr_lim_u(pr_lim_u_mn, pr_lim_u_mx):
    """Create CAN message object with data loaded."""
    payload = None
    msgfmt = SET_PR_LIM_U["msg_fmt"]
    msgid = SET_PR_LIM_U["msg_id"]
    payload = struct.pack(msgfmt, pr_lim_u_mn, pr_lim_u_mx)
    logger.debug("Message payload: %s", payload)
    return Message(arbitration_id=msgid, data=payload, extended_id=False)


def load_set_pr_lim_i(pr_lim_i_mn, pr_lim_i_mx):
    """Create CAN message object with data loaded."""
    payload = None
    msgfmt = SET_PR_LIM_I["msg_fmt"]
    msgid = SET_PR_LIM_I["msg_id"]
    payload = struct.pack(msgfmt, pr_lim_i_mn, pr_lim_i_mx)
    logger.debug("Message payload: ", binascii.hexlify(payload))
    return Message(arbitration_id=msgid, data=payload, extended_id=False)


def load_set_pr_lim_pwr(pr_lim_pwr_mn, pr_lim_pwr_mx):
    """Create CAN message object with data loaded."""
    payload = None
    msgfmt = SET_PR_LIM_PWR["msg_fmt"]
    msgid = SET_PR_LIM_PWR["msg_id"]
    payload = struct.pack(msgfmt, pr_lim_pwr_mn, pr_lim_pwr_mx)
    logger.debug("Message payload: ", binascii.hexlify(payload))
    return Message(arbitration_id=msgid, data=payload, extended_id=False)


"""

    F U N C T I O N S   T O   U N L O A D   D A T A   F R O M   C A N   M E S S A G E S 

"""

def unload_set_slope_u_i(msg):
  """Return CAN message data from message object."""
  msgfmt = SET_SLOPE_U_I["msg_fmt"]
  voltage, current = struct.unpack(msgfmt, msg.data)
  return (voltage, current)


"""

    A U X I L I A R Y   F U N C T I O N S

"""


def set_bit(shift, value, bitmask):
    return (value << shift) & bitmask


def clear_bit(shift, value, bitmask):
    return (value << shift) ^ bitmask


"""

    C L A S S E S

"""
