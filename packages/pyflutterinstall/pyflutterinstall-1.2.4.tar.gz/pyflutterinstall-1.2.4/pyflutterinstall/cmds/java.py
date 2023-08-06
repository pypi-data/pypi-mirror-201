"""
Command stub for sdkmanager
"""

import os
import sys

from pyflutterinstall.config import config_load
from pyflutterinstall.trampoline import trampoline

JAVA_DIR = config_load().get("JAVA_DIR", "INVALID")

COMMAND = "java"


def find_default_path_or_none() -> str | None:
    """Find default path"""
    jdk_folders = os.listdir(JAVA_DIR)
    if not jdk_folders:
        return None
    if len(jdk_folders) > 1:
        jdk_folders.sort()
        jdk_folders.reverse()
    return os.path.join(JAVA_DIR, jdk_folders[0], "bin")


def main(argv: list[str] | None = None) -> int:
    """Main"""
    return trampoline(COMMAND, args=argv, default_path=find_default_path_or_none())


if __name__ == "__main__":
    sys.exit(main())
