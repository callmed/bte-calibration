#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

"""
Comment style description of the script's purpose.

FILE_STRUCTURE: main.py: Contains general program parts like console argument handling, filesystem jobs, CAN interface handling.
				calibration.py: Contains basic information, required for the calibration process. E.g. writing the calibration protocol
								sending messages,
				messages.py: Provides message details, generates messages and converts message data back into raw values.

Arguments:
    --version:     Show software version
    --debug:        Activates debugging messages into a logfile

"""

#TODO: Check argument list items exists and raise an error if not. (Bitrate, Device)


import sys, os, argparse
import can
import logging


SW_VERION = 0.1
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, "cfg")
LOOPBACK_DEVICE = True      # Second interface channel for sw-testing

"""Enviroment variable to get a default logging configuration file."""
#env_key = "LOG_CFG"
#print(os.getenv(env_key, None))

if os.path.exists(os.path.join(CONFIG_DIR, "logging.yaml")):
    import yaml
    import logging.config

    with open(os.path.join(CONFIG_DIR, "logging.yaml"), "rt") as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
else:
    print("no logging config file found")
    frm = logging.Formatter("[{levelname:8}] {asctime} : [FROM: {module} <- {funcName}] : [{name}] -> {message}",
                            "%d.%m.%Y %H:%M:%S", style="{")
    # Setup for file logging
    logfile_name = __file__[:-3] + ".log"
    fh = logging.FileHandler(filename=logfile_name, mode='w', delay=True)
    fh.setFormatter(frm)
    fh.setLevel(logging.WARNING)
    # Setup for console logging
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(frm)
    ch.setLevel(logging.DEBUG)
    # logger.addHandler(fh) # activated via console command
    #logger.addHandler(ch)

logger = logging.getLogger("calibration")
#logger.setLevel(logging.DEBUG)
# Configure module logger object


import tas_protocol as tas  # Initialized here to make the logger objects working at module level


class InvalidArguments(Exception):
    """Used for provided invalid console arguments."""
    pass


def dummyA(*args, **kwargs):
    pass



def main():
    logger.info("*** BTE Calibration Tool ***\n")
    appRunning = True
    logger_can = logging.getLogger('canlogger')
    logger_can.debug("CAN LOGGER created")

    """
        W R I T E   C O D E   H E R E
    """

    l = can.CSVWriter(filename="test.csv")
    while appRunning:
        try:

            for msg in tas.macroBTE_Initialization(slope_u_i_pwr=(200,200,200),
                                                   limit_mn_u_i_pwr=(0,600,200),
                                                   limit_mx_u_i_pwr=(0,600,200)):
                logger_can.info(msg)
                can_device.send(msg)


            for msg in lp_device:
                print(msg)


            appRunning = False
            logger.info("Program will quit here")

        except can.CanError as e:
            logger.error("Error occurred while CAN interface was active. %s", e)

        except KeyboardInterrupt:
            logger.info("User quit program!")
            appRunning = False

    print("Program exit")


if __name__ == "__main__":

    logger.debug("Base directory: %s", BASE_DIR)
    logger.debug("Log configuration directory: %s", CONFIG_DIR)

    # Read console arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="store_true", default=False, dest="sw_version",
                        help="Print software version")
    #TODO: Add location to CAN logfile
    args = parser.parse_args()
    try:
        if args.sw_version:
            print("BTE Calibration Tool - v{}".format(SW_VERION))
            sys.exit(0)

    except InvalidArguments as e:
        logger.error("Invalid argument provided")
        sys.exit(1)

    """Create a CAN device based on available configuration methodes.
    Only the root directory can be used to load the interface configuration. 
    Otherwise an error is raised when creating the can.Bus() object.
    """
    try:
        if os.path.exists("can.ini"):
            logger.debug("Loading CAN device settings from file")
            can.util.load_file_config()
            can_device = can.Bus()
        else:
            logger.warning("CAN device configuration file not found")
            can.rc["interface"] = tas.CAN_INTERFACE
            can.rc["channel"] = tas.CAN_CHANNEL
            can.rc["bitrate"] = tas.CAN_BITRATE
            can_device = can.interface.Bus()
    except can.CanError as e:
            logger.error("Failure during creating CAN device %s", e)
    else:
        logger.info("CAN device created: %s", can_device)

    if LOOPBACK_DEVICE:
        lp_device = can.interface.Bus(bustype=tas.CAN_DEVICES["kvaser"],
                                      channel=1,
                                      bitrate=tas.CAN_BITRATES["500K"])
        logger.debug("Loopback-Interface: %s", lp_device)

    main()
