"""
Unit test file.
"""

import os
import unittest

from pyflutterinstall.cmds import adb, avdmanager, emulator, gradle, java, sdkmanager

# config
from pyflutterinstall.config import config_load

config = config_load()
INSTALLED = config.get("INSTALL_DIR") is not None


class UseExePaths(unittest.TestCase):
    """Thest that each tool can be called from the path."""

    @unittest.skipIf(not INSTALLED, "Not installed")
    def test_java(self) -> None:
        """Tests that we can bind to the java executable."""
        print("Test java")
        self.assertEqual(0, java.main(["-version"]))

    @unittest.skipIf(not INSTALLED, "Not installed")
    def test_adb(self) -> None:
        """Tests that we can bind to the adb executable."""
        print("Test adb")
        self.assertEqual(0, adb.main(["version"]))

    @unittest.skipIf(not INSTALLED, "Not installed")
    def test_avdmanager(self) -> None:
        """Tests that we can bind to the avdmanager executable."""
        print("Test avdmanager")
        self.assertEqual(1, avdmanager.main(["--help"]))

    @unittest.skipIf(not INSTALLED, "Not installed")
    def test_gradle(self) -> None:
        """Tests that we can bind to the gradle executable."""
        print("Test gradle")
        os.system("printenv")
        self.assertEqual(0, gradle.main(["-version"]))

    @unittest.skipIf(not INSTALLED, "Not installed")
    def test_sdkmanager(self) -> None:
        """Tests that we can bind to the sdkmanager executable."""
        print("Test sdkmanager")
        self.assertEqual(1, sdkmanager.main(["--help"]))

    @unittest.skipIf(not INSTALLED, "Not installed")
    def test_emulator(self) -> None:
        """Tests that we can bind to the emulator executable."""
        print("Test emulator")
        self.assertEqual(0, emulator.main(["-help"]))


if __name__ == "__main__":
    unittest.main()
