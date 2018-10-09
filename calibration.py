#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#TODO:
#TODO:

"""
Comment style description of the script's purpose.

"""

import numpy as np
from messages import *


CAN_BITRATES = {
					"1M":1000000,
					"500K":500000,
					"250":250000,
					"125K":125000
				}
				
CAN_DEVICES = {
					"kvaser":"kvaser",
					"vector":"vector",
					"pcan":"pcan",
					"ixxat":"ixxat"
			}

				
# ENVIROMENT VARIABLE for CAN interfaces
CAN_INTERFACE = "kvaser"
CAN_CHANNEL = 0
CAN_BITRATE = CAN_BITRATES["500K"]

#if CAN_INTERFACE not NULL:
#    can.util.load_environment_config()

# Manual configuration of CAN interface
#can.rc['interface'] = CAN_DEVICES["kvaser"]
#can.rc['channel'] = 0
#can.rc['bitrate'] = CAN_BITRATE["500K"]

# Or in one line
#can_interface_receiver = can.interface.Bus(bustype=CAN_DEVICES["kvaser"], channel=1, bitrate=CAN_BITRATE["500K"])

# Load CAN interface from configuration file
#LOC_INTERFACE_CONFIGFILE="can.ini"
#config_interface = can.util.load_file_config(LOC_INTERFACE_CONFIGFILE)

#can_interface = can.Bus()

#bus = can.interface.Bus()



"""
    MACROS WITH PRE-DEFINED MESSAGES FOR CALIBRATION
"""

macro_initiate_BTE = [
    load_message(_id=SET_SLOPE_U_I["msg_id"], fmt=SET_SLOPE_U_I["msg_fmt"], voltage_slope=200, current_slope=200),
    load_set_slope_pwr_filter(slope_power=200, filter=0),
    load_set_op_lim_u(op_lim_u_mn=0,op_lim_u_mx=1400),
    load_set_op_lim_i(op_lim_i_mn=-900,op_lim_i_mx=900),
    load_set_op_lim_pwr(op_lim_pwr_mn=-500,op_lim_pwr_mx=500),
    load_set_pr_lim_u(pr_lim_u_mn=0,pr_lim_u_mx=1400),
    load_set_pr_lim_i(pr_lim_i_mn=-900,pr_lim_i_mx=900),
    load_set_pr_lim_pwr(pr_lim_pwr_mn=-500,pr_lim_pwr_mx=500),
    load_clearance(clearance=1),
    load_set_rst_stop(rst_stop=1)
]


def convert2_IEEE754Hex32(value):
    """Converts a float value into a IEEE-754 hex representative value."""
    try:
        return hex(np.float32(float(value)).view(np.int32).item())
    except TypeError as e:
        print(e)
