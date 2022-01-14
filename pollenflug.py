#!/bin/env python3
"""This script/program fetches the pollen prediction calendar from Hexal and prints to CLI"""
# Command line args and exit codes
import sys
import os
import getopt

# For dict/r.json type hinting
from typing import Dict, Type

# Enum type for colors
from enum import Enum

# Parser for INI config files and homedir
import configparser
from pathlib import Path

# HTTP requests and parsing
from datetime import datetime
import requests

REQ_URL = "https://allergie.hexal.de/pollenflug/vorhersage/load_pollendaten.php"
ENG_LIST = ["Ambrosia", "Dock", "Artemisia", "Birch", "Beech", "Oak", "Alder", "Ash", "Grass",
            "Hazel", "Popplar", "Rye", "Elm", "Plantain", "Willow"]

# Define input options
SHORT_OPT = "d:p:hve"
LONG_OPT = ["date=", "plz=", "help", "verbose", "english"]
arg_list = sys.argv[1:]

# Config absolute directory
CONFIG_LOCATION = str(Path.home()) + "/.pollenflug.ini"


def print_help() -> None:
    """Print help menu with argument, usage, copyright and Github"""
    print("""Usage: pollenflug.py [options]

    -h,--help               Print this help menu
    -d,--date=YYYY-MM-DD    Set start date of pollen calendar
    -p,--plz=iiiii          Set postal code/plz
    -e,--english            Print plant names in English
    -v,--verbose            Print verbose


By default, date is set to today and plz to Hamburg.
Data is fetched from Hexal's Pollenflugkalendar.

pollenflug  Copyright (C) 2021  Bader Zaidan
This program comes with ABSOLUTELY NO WARRANTY;
This is free software, and you are welcome to redistribute it
under certain conditions; read LICENSE for details.

For bug reports and feature requests, see:
https://github.com/BaderSZ/pollenflug""")


class Color(Enum):
    """Color class we can use to instead of literals"""
    GREEN = "0"
    ORANGE, ORANGE_TOO = "1", "2"
    RED = "3"


def format_color(string: str, color: Type[Color]) -> str:
    """Give each pollen value an appropriate color in the table"""
    green = '\033[92m'
    orange = '\033[93m'
    red = '\033[91m'
    endc = '\033[0m'

    if color == Color.GREEN:
        return green + string + endc
    if color in (Color.ORANGE, Color.ORANGE_TOO):
        return orange + string + endc
    if color == Color.RED:
        return red + string + endc
    return string


def print_calendar(data: Dict, eng: bool = False) -> None:
    """Print calendar as a table with appropriate spacing"""
    # Print top Bar:
    print("Date", end="\t\t")
    if eng:
        for string in ENG_LIST:
            print(string[:6], end="\t")
    else:
        for string in data["content"]["pollen"]:
            print(string[:6], end="\t")
    print()  # Newline

    # Loop, print for every date
    for string in data["content"]["values"]:
        cdate = string
        print(cdate, end="\t")
        for val in data["content"]["values"][cdate]:
            print(format_color(val, Color(val)), end="\t")
        print()  # Newline


def loadconfig(config_location: str) -> (int, bool, bool):
    """Function to check for a config file and check/load it."""
    # Load config file
    config = configparser.ConfigParser()
    config.read(config_location)

    if not Path(config_location).exists():
        return 20095, True, False

    # Check config file for postal code, and set appropriately
    try:
        plz = int(config['DEFAULT']['plz'])
    except TypeError:
        # plz not defined in config file, use default
        plz = 20095
    except ValueError:
        print(format_color("Error", Color.RED) +
              ": invalid postal code in config!")
        sys.exit(os.EX_CONFIG)
    except KeyError:
        print("Unknown error, could not process postal code in config!")
        sys.exit(os.EX_CONFIG)

    # Check config file for debug flag, and set appropriately
    try:
        debug_str = config['DEFAULT']['debug'].lower()
        if debug_str in ("true", "1"):
            debug = True
        elif debug_str in ("false", "0", ""):
            debug = False
        else:
            print(format_color("Error", Color.RED) +
                  ": invalid debug flag in config!")
            sys.exit(os.EX_CONFIG)
    except KeyError:
        print(format_color("Unknown Error", Color.RED) +
              ": could not process debug flag in config")
        sys.exit(os.EX_CONFIG)

    # Check config file for english flag, and set if given.
    try:
        eng = config['DEFAULT']['en'].lower()
        if eng in ("true", "1"):
            use_eng = True
        elif eng in ("false", "0", ""):
            use_eng = False
        else:
            print(format_color("Error", Color.RED) +
                  ": invalid language flag in config!")
            sys.exit(os.EX_CONFIG)
    except KeyError:
        print(format_color("Unknown Error", Color.RED) +
              ": could not process language flag in config")
        sys.exit(os.EX_CONFIG)

    return plz, use_eng, debug


def main() -> None:
    """main() function, parse arguments and call functions"""
    # Default values
    date = datetime.today().strftime("%Y-%m-%d")
    history = "no"

    # Load config, with default values
    plz, use_eng, debug = loadconfig(CONFIG_LOCATION)

    # Check CLI options, exit if undefined
    try:
        arguments, _val = getopt.getopt(arg_list, SHORT_OPT, LONG_OPT)
    except getopt.error as exp:
        print(format_color("Error", Color.RED) + ": Invalid input arguments!")
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
        print(format_color("Error", Color.RED) + ": Failed sending request.")
        if debug:
            print(exp)
        sys.exit(os.EX_SOFTWARE)

    json_data = request.json()
    if json_data["message"] != "success":
        print(format_color("Error", Color.RED) +
              ": Server error. Check your arguments?")
        sys.exit(os.EX_SOFTWARE)

    # Print results
    print("Data for " + str(plz) + ", Germany")
    print_calendar(json_data, eng=use_eng)
    sys.exit(os.EX_OK)


if __name__ == "__main__":
    main()
