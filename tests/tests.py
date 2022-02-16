"""Test module for pollenflug. Make sure changes work before pushing"""

import sys

from pathlib import Path
import unittest

DIR = str(Path(__file__).parent.resolve())
sys.path.append(DIR + "/../")

from lib.functions import loadconfig
from lib.color import Color


class TestStringMethods(unittest.TestCase):
    """Unit test class containing test functions.

    So far, only 1 class and one function are tested.
    """

    def test_colors(self):
        """Test the Color class. Specifically go for:

        - format_color() function
        - value to Enum conversion
        """
        # Test default = no coloring
        self.assertEqual(Color.format_color("Hello, World!"), "Hello, World!")

        # Test color<-> number conversion
        self.assertEqual(Color("0"), Color.GREEN)
        self.assertEqual(Color("1"), Color.ORANGE)
        self.assertEqual(Color("2"), Color.ORANGE_TOO)
        self.assertEqual(Color("3"), Color.RED)

        # Test some function colors
        self.assertEqual(Color.format_color("Hello, nothing!"), "Hello, nothing!")
        self.assertEqual(Color.format_color(
            "Hello, Red!", Color.RED), "\033[91mHello, Red!\033[0m")
        self.assertEqual(Color.format_color(
            "Hello, Green!", Color.GREEN), "\033[92mHello, Green!\033[0m")
        self.assertEqual(Color.format_color("Hello, Orange!",
                                            Color.ORANGE), "\033[93mHello, Orange!\033[0m")

    def test_config(self):
        """Test config loading. Both with and without file"""

        # Test without a config
        plz, eng, debug = loadconfig("/tmp/fakeconfigfile69420")

        self.assertEqual(plz, 20095)
        self.assertEqual(eng, True)
        self.assertEqual(debug, False)

        # Test using the test config.
        plz, eng, debug = loadconfig(DIR + "/testconfig.ini")

        self.assertEqual(plz, 55555)
        self.assertEqual(eng, False)
        self.assertEqual(debug, True)

        # Test using 2nd config.
        # Note! default values should be used for undefined entries
        plz, eng, debug = loadconfig(DIR + "/testconfig_missingval.ini")

        self.assertEqual(plz, 44331)
        self.assertEqual(eng, False)
        self.assertEqual(debug, False)


if __name__ == '__main__':
    unittest.main()
