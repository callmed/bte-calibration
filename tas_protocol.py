#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#TODO:
#TODO:
""" Communication protocol implementation.

"""

import messages as msg
import logging

logger = logging.getLogger("calibration.protocol")
logger.setLevel(logging.DEBUG)


"""Available CAN bitrates for communication"""
CAN_BITRATES = {"1M": 1000000,
                "500K": 500000,
                "250": 250000,
                "125K": 125000
                }


"""Supported CAN devices"""
CAN_DEVICES = {"kvaser": "kvaser",
               "vector": "vector",
               "pcan": "pcan",
               "ixxat": "ixxat"
               }


CAN_INTERFACE = "kvaser"
CAN_CHANNEL = 0
CAN_BITRATE = CAN_BITRATES["500K"]


"""

    P R E - D E F I N E D   M A C R O S   F O R   C A L I B R  A T I O N

"""


"""List of  Setup values are provided as tuple for voltage, current and power
    """

def macroBTE_Initialization(slope_u_i_pwr: tuple, limit_mn_u_i_pwr: tuple, limit_mx_u_i_pwr: tuple):
    """ CAN message to setup BTE for calibration.

    Setup values are provided as tuple.
    :param slope_u_i_pwr: Tuple to setup slope values of voltage, current and power
    :param limit_mn_u_i_pwr: Tuple to setup minimum limit values of voltage, current and power
    :param limit_mx_u_i_pwr: Tuple to setup maximum limit values of voltage, current and power
    :return: List of CAN messages
    """
    slope_voltage = None
    slope_current = None
    slope_pwr = None
    limit_mn_voltage = None
    limit_mn_current = None
    limit_mn_pwr = None
    limit_mx_voltage = None
    limit_mx_current = None
    limit_mx_pwr = None

    yield msg.load_message(msg.SET_SLOPE_U_I, slope_voltage=200, slope_current=200)
    yield msg.load_message(msg.SET_SLOPE_PWR_FILTER, slope_power=200, filter=0)
    yield msg.load_message(msg.SET_OP_LIM_U, U_MX=1400, U_MIN=0)
    yield msg.load_message(msg.SET_OP_LIM_I, I_MN=-900, I_MX=900)
    yield msg.load_message(msg.SET_OP_LIM_PWR, PWR_MN=-500, PWR_MX=500)
    yield msg.load_message(msg.SET_PR_LIM_I, I_MN=-900, I_MX=900)
    yield msg.load_message(msg.SET_PR_LIM_PWR, PWR_MN=-500, PWR_MX=500)
    yield msg.load_message(msg.SET_PR_LIM_U, U_MN=0, U_MX=1400)
    yield msg.load_message(msg.CLEARANCE, clearance=1)
    yield msg.load_message(msg.SET_RST_STOP, rst_stop=1)
    """Missing messages for initialization: send_msg, debug_enable, debug_send=1, debug_send=0, 
    hai_enablecontrol, hai_resetError, hai_set_state
    """


def macroBTE_Calibrate800V():
    """List of CAN messages to run a 800V calibration curve.
    Message list:   1. set ctrl-mode to voltage
                    2. set operational limits
                    3. set slope values
                    4. set protectional limits
                    5. send clearance
                    6. send set_rst_stop
                    7. send switch-to-ON

    """
    pass


"""

    F U N C T I O N S

"""

def set_register_ref_switch_ctrl_ri(set_ref,set_switch,set_ctrl,rst_q=False,rst_e=False,set_ri=0):
    """ Takes values to change the EStorage state and controller and set set values of controller.

    :param set_ref: Set value of controller, based on the active controller mode
    :param set_switch: Change the EStorage state between Off, Standby and On
    :param set_ctrl: Change controller mode according to the manual
    :param rst_q: Reset the value of q
    :param rst_e: Reset the value of energy
    :param set_ri: Set an inner resistance
    :return: returns a CAN message with id=0xC1
    """
    from can import Message
    from struct import pack

    try:
        _reference_value = pack("<f", set_ref)
        if 0 <= set_switch <= 7:
            _operating_state = set_switch
        else:
            raise ValueError
        if 0 <= set_ctrl <= 7:
            _control_mode = set_ctrl
        else:
            raise ValueError
        if -2000 <= set_ri <= 2000:
            _resistance_ri = pack("<f", set_ri)[:3]
        else:
            raise ValueError

    except msg.struct.error:
        logger.error("Error occurred while packing data", exc_info=True)
        return None
    except ValueError:
        logger.error("Wrong parameter value provided in function", exc_info=True)
        return None

    reg_ctrl = _operating_state << 0
    reg_ctrl += (_control_mode << 3)
    reg_ctrl += (rst_q << 6)
    reg_ctrl += (rst_e << 7)
    logger.debug("Byte value of REG_CTRL: %s", bin(reg_ctrl))

    payload = _reference_value + bytes([reg_ctrl]) + _resistance_ri
    logger.debug("Payload for message := %s", payload)
    return Message(arbitration_id=0xC1, data=payload, extended_id=False)


# CANID: 0x288
def request_system_status():
    pass


# CANID: 0xFE manual page 35
def request_system_info():
    pass


def reset_stop(value=False):
    from can import Message
    from struct import pack
    _id = 0x21F
    try:
        #TODO: Check current system status
        """ Check system status because: 
                    Standby-Errors require OFF or SBY 
                    Critical-Errors require OFF
           
           Status information is available in messages 0x518 and 0x528
        """
        if 0 <= value <= 255:
            return Message(arbitration_id=_id, data=pack("<B", value), extended_id=False)
        else:
            raise ValueError

    except ValueError:
        logger.error("Wrong parameter value provided in function", exc_info=True)
        return None
