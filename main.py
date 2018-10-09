#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#TODO: Check argument list items exists and raise an error if not. (Bitrate, Device)
#TODO: Update comments

"""
Comment style description of the script's purpose.

FILE_STRUCTURE: main.py: Contains general program parts like console argument handling, filesystem jobs, CAN interface handling.
				calibration.py: Contains basic information, required for the calibration process. E.g. writing the calibration protocol
								sending messages,
				messages.py: Provides message details, generates messages and converts message data back into raw values.

Arguments:
    --software:     Show software version
    --debug:        Activate debugging

"""


import os
import sys
import logging
import argparse
import can
import calibration
import messages


SW_VERION = 0.1
LOOPBACK_DEVICE = True      # Second interface channel for sw-testing
logger = logging.getLogger("bte-calib." + __name__)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#GUI_DIR = os.path.join(BASE_DIR,"gui")


class InvalidArguments(Exception):
    pass


def main():
    # Configure module logger object
    frm = logging.Formatter("[{levelname:8}] {asctime} : {name} : {funcName} : {message}", "%d.%m.%Y %H:%M:%S", style="{")
    # Setup for file logging
    logfile_name = __file__[:-3] + ".log"
    fh = logging.FileHandler(filename=logfile_name, mode='w', delay=True)
    fh.setFormatter(frm)
    fh.setLevel(logging.ERROR)
    # Setup for console logging
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(frm)
    ch.setLevel(logging.WARNING)
    global logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.setLevel(logging.DEBUG)

    # Read console arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", default=False, dest="sw_debug",
                        help="Activate debugging into logfile")
    parser.add_argument("--version", action="store_true", default=False, dest="sw_version",
                        help="Print software version")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true", dest="verbose", help="Write detailed console info text.")
    group.add_argument("-q", "--quiet", action="store_true", dest="quiet", help="Only critical message to console")
    parser.add_argument("--device", action="store", dest="device", help="Define CAN interface")
    parser.add_argument("--bitrate", action="store", dest="bitrate",
                        help="CAN bitrate. Possible values: 1M, 500K, 250K, 125K")
    parser.add_argument("--channel", action="store", choices=["0", "1"], dest="channel",
                        help="Set CAN channel of interface. Possible values: 0, 1")
    #TODO: Add location to CAN logfile
    #TODO: Add location to CAN interface configuration file
    args = parser.parse_args()

    try:
        if args.sw_debug:
            logger.setLevel(logging.DEBUG)
            ch.setLevel(logging.DEBUG)
            fh.setLevel(logging.DEBUG)
            logger.debug("Debugging active")
        else:
            logger.setLevel(logging.DEBUG)
            ch.setLevel(logging.ERROR)
            fh.setLevel(logging.ERROR)

        if args.sw_version:
            print("BTE Calibration Tool - v{}".format(SW_VERION))
            sys.exit(0)

        if args.verbose:
            ch.setLevel(logging.INFO)
        elif args.quiet:
            ch.setLevel(logging.CRITICAL)

        if args.device:
            if args.device in calibration.CAN_DEVICES:
                 calibration.CAN_INTERFACE = args.device
                 logger.info("Set CAN device: >>{}<<".format(calibration.CAN_INTERFACE))
            else:
                logger.error("CAN device not supported")

        if args.channel:
            calibration.CAN_CHANNEL = int(args.channel)
            logger.info("Set CAN channel: >>{}<<".format(calibration.CAN_CHANNEL))

        if args.bitrate:
            if args.bitrate in calibration.CAN_BITRATES:
                calibration.CAN_BITRATE = args.bitrate
                logger.info("Set CAN bitrate: >>{}<<".format(calibration.CAN_BITRATE))
            else:
                logger.error("Bitrate not supported")


    except InvalidArguments as e:
        logger.error("Invalid argument provided")
        sys.exit(1)



    #
    # RUN CODE HERE
    #

    logger.debug("Running program code")

    try:
        if args.channel or args.device or args.bitrate:
            logger.debug("User interface configuration set")
            # Create CAN interface object based on user defined setup
        else:
            config_interface = can.util.load_file_config()
            logger.debug("Loading interface settings: >>{}<<".format(config_interface))

        interface = can.Bus()
        if LOOPBACK_DEVICE:
            interface_loopback = can.interface.Bus(bustype=calibration.CAN_INTERFACE, channel=1,
                                                   bitrate=calibration.CAN_BITRATE)

    except FileNotFoundError as e:
        logger.error("CAN configuration file not found", e)

    except can.CanError as e:
        logger.error("CAN error occurred during setup", e)


    while True:


        for msg in calibration.macro_initiate_BTE:
            interface.send(msg)

        while True:
            try:
        #
        #    #Send CAN messages
        #    for msg in lst_canmessages:
        #        can_sender.send(msg)

                #Receive CAN messages
                for msg in interface_loopback:
                    print(msg)

            except can.CanError:
                logger.error("CAN message nocht sent!")
            except KeyboardInterrupt:
                logger.info("Interrupted by user!")


if __name__ == "__main__":
    main()
