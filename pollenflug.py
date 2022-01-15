#!/bin/env python3
"""This script/program fetches the pollen prediction calendar from Hexal and prints to CLI"""
# Command line args and exit codes
import sys
import os
import getopt

# Parser for INI config files and homedir
from pathlib import Path

# HTTP requests and parsing
from datetime import datetime
import requests

# local
from functions import loadconfig, print_calendar, print_help
from consts import LONG_OPT, SHORT_OPT, REQ_URL
from color import Color

# Config absolute directory
CONFIG_LOCATION = str(Path.home()) + "/.pollenflug.ini"


def main() -> None:
    """main() function, parse arguments and call functions"""
    # Default values
    date = datetime.today().strftime("%Y-%m-%d")
    history = "no"

    # Define input options
    arg_list = sys.argv[1:]

    # Load config, with default values
    plz, use_eng, debug = loadconfig(CONFIG_LOCATION)

    # Check CLI options, exit if undefined
    try:
        arguments, _val = getopt.getopt(arg_list, SHORT_OPT, LONG_OPT)
    except getopt.error as exp:
        print(Color.format_color("Error") + ": Invalid input arguments!")
        if debug:
            print(exp)
        print_help()
        sys.exit(os.EX_USAGE)

    # Set CLI arguments.
    for arg, val in arguments:
        if arg in ("-d", "--date"):
            date = val
            history = "yes"
        elif arg in ("-p", "--plz"):
            plz = val
        elif arg in ("-v", "--verbose"):
            debug = True
        elif arg in ("-h", "--help"):
            print_help()
            sys.exit(os.EX_OK)
        elif arg in ("-e", "--english"):
            use_eng = True

    req_load = {"datum": date, "plz": plz, "historie": history}

    # Get data from HEXAL, exception if error
    try:
        request = requests.post(REQ_URL,  params=req_load)
    except requests.exceptions.RequestException as exp:
        print(Color.format_color("Error") + ": Failed sending request.")
        if debug:
            print(exp)
        sys.exit(os.EX_SOFTWARE)

    json_data = request.json()
    if json_data["message"] != "success":
        print(Color.format_color("Error") +
              ": Server error. Check your arguments?")
        sys.exit(os.EX_SOFTWARE)

    # Print results
    print("Data for " + str(plz) + ", Germany")
    print_calendar(json_data, eng=use_eng)
    sys.exit(os.EX_OK)


if __name__ == "__main__":
    main()
