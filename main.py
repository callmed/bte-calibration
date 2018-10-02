#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#TODO:
#TODO:

"""
Comment style description of the script's purpose.

Arguments:
    --software:     Show software version
    --debug:        Activate debugging

"""


import os
import sys
import logging
import argparse


SW_VERION = 0.1
DEBUGGING = False
LOGGER = logging.getLogger(__name__)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GUI_DIR = os.path.join(BASE_DIR,"gui")


class InvalidArguments(Exception):
    pass


def main():
    # Configure module logger object
    frm = logging.Formatter("[{levelname:8}] {asctime} : {funcName} : {message}","%d.%m.%Y %H:%M:%S", style="{")
    logger = LOGGER
    logger.setLevel(logging.DEBUG)
    # Setup for file logging
    logfile_name = __file__[:-3] + ".log"
    fh = logging.FileHandler(filename=logfile_name, mode='w', delay=True)
    fh.setFormatter(frm)
    fh.setLevel(logging.ERROR)
    logger.addHandler(fh)
    # Setup for console logging
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(frm)
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    # Read console arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", default=False, dest="sw_debug", help="Activate debugging into logfile")
    parser.add_argument("--version", action="store_true", default=False, dest="sw_version", help="Print software version")
    args = parser.parse_args()

    try:
        if args.sw_version:
            print("BTE Calibration Tool - v{}".format(SW_VERION))
            sys.exit(0)

        if args.sw_debug:
            DEBUGGING = True
            logger.debug("Debugging active")

    except InvalidArguments as e:
        logger.error("Invalid argument")
        sys.exit(1)

    else:
        logger.debug("Provided argument valid")
        # RUN CODE HERE


if __name__ == "__main__":
    main()
