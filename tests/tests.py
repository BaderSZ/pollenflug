"""Test module for pollenflug. Make sure changes work before pushing"""

import sys

from pathlib import Path

DIR = str(Path(__file__).parent.resolve())
sys.path.append(DIR + "/../")

from pollenflug.lib.functions import loadconfig
from pollenflug.lib.color import Color


def test_colors():
    """Test the Color class. Specifically go for:

    - format_color() function
    - value to Enum conversion
    """
    # Test default = no coloring
    assert Color.format_color("Hello, World!") == "Hello, World!"

    # Test color<-> number conversion
    assert Color("0") == Color.GREEN
    assert Color("1") == Color.ORANGE
    assert Color("2") == Color.ORANGE_TOO
    assert Color("3") == Color.RED

    # Test some function colors
    assert Color.format_color("Hello, nothing!") == "Hello, nothing!"
    assert Color.format_color("Hello, Red!", Color.RED) == "\033[91mHello, Red!\033[0m"
    assert (
        Color.format_color("Hello, Green!", Color.GREEN)
        == "\033[92mHello, Green!\033[0m"
    )
    assert (
        Color.format_color("Hello, Orange!", Color.ORANGE)
        == "\033[93mHello, Orange!\033[0m"
    )


def test_config():
    """Test config loading. Both with and without file"""

    # Test without a config
    plz, eng, debug = loadconfig("/tmp/fakeconfigfile69420")

    assert plz == 20095
    assert eng == True
    assert debug == False

    # Test using the test config.
    plz, eng, debug = loadconfig(DIR + "/testconfig.ini")

    assert plz == 55555
    assert eng == False
    assert debug == True

    # Test using 2nd config.
    # Note! default values should be used for undefined entries
    plz, eng, debug = loadconfig(DIR + "/testconfig_missingval.ini")

    assert plz == 44331
    assert eng == False
    assert debug == False
