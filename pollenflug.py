#!/bin/env python3
"""This script/program fetches the pollen prediction calendar from Hexal and prints to CLI"""
# Command line args and exit codes
import sys
import os
import getopt

# HTTP requests and parsing
from datetime import datetime
import requests

# For dict/r.json type hinting
from typing import Dict

REQ_URL = "https://allergie.hexal.de/pollenflug/vorhersage/load_pollendaten.php"
ENG_LIST = ["Ambrosia","Dock","Artemisia","Birch","Beech","Oak","Alder","Ash","Grass","Hazel","Popplar","Rye","Elm","Plantain","Willow"]

# Define input options
SHORT_OPT = "d:p:hve"
LONG_OPT  = ["date=", "plz=", "help", "verbose", "english"]
arg_list = sys.argv[1:]

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


def format_color(s: str) -> str:
    """Give each pollen value an appropriate color in the table"""
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

    if s == "0":
        return GREEN+s+ENDC
    elif s in ("1", "2"):
        return ORANGE+s+ENDC
    elif s == "3":
        return RED+s+ENDC
    else:
        return s

def print_calendar(data: Dict, eng: bool = False) -> None:
    """Print calendar as a table with appropriate spacing"""
    # Print top Bar:
    print("Date", end="\t\t")
    if eng:
        for s in ENG_LIST:
            print(s[:6], end="\t")
    else:
        for s in data["content"]["pollen"]:
            print(s[:6], end="\t")
    print() # Newline

    # Loop, print for every date
    for s in data["content"]["values"]:
        cdate = s
        print(cdate, end="\t")
        for v in data["content"]["values"][cdate]:
            print(format_color(v), end="\t")
        print()


def main() -> None:
    """main() function, parse arguments and call functions"""
    # Default values
    date = datetime.today().strftime("%Y-%m-%d")
    plz = 20095
    debug = False
    eng_list = False

    try:
        arguments, _val = getopt.getopt(arg_list, SHORT_OPT, LONG_OPT)
    except getopt.error as e:
        print("\033[91mError\033[0m: Invalid input arguments!")
        if debug:
            print(e)
        print_help()
        sys.exit(os.EX_USAGE)

    for arg, val in arguments:
        if arg in ("-d", "--date"):
            date = val
        elif arg in ("-p", "--plz"):
            plz = val
        elif arg in ("-v", "--verbose"):
            debug = True
        elif arg in ("-h", "--help"):
            print_help()
            sys.exit(os.EX_OK)
        elif arg in ("-e", "--english"):
            eng_list = True

    req_load = {"datum": date, "plz": plz}

    try:
        r = requests.post(REQ_URL,  params=req_load)
    except requests.exceptions.RequestException as e:
        print("\033[91mError\033[0m: Failed sending request.")
        if debug:
            print(e)
        sys.exit(os.EX_SOFTWARE)

    json_data = r.json()
    if json_data["message"] != "success":
        print("\033[91mError\033[0m: Server error. Check your arguments?")
        sys.exit(os.EX_SOFTWARE)

    print("Data for " + str(plz) + ", Germany")
    print_calendar(json_data, eng=eng_list)
    sys.exit(os.EX_OK)


if __name__ == "__main__":
    main()
