"""
Test pyflutterinstall
"""

import unittest
import os


class PyflutterinstallTester(unittest.TestCase):
    """Tests pyflutterinstall"""

    def test_platform_executable(self) -> None:
        """Tests the platform executable"""
        rtn = os.system("pyflutterinstall --help")
        self.assertEqual(rtn, 0)


if __name__ == "__main__":
    unittest.main()
