"""
Command stub for sdkmanager
"""
import os
import sys

from pyflutterinstall.trampoline import trampoline
from pyflutterinstall.config import config_load

config = config_load()
android_sdk = config.get("ANDROID_SDK", ".")

if android_sdk != ".":
    os.environ["ANDROID_SDK"] = android_sdk
    os.environ["ANDROID_HOME"] = android_sdk

COMMAND = "adb"
DEFAULT_PATH = os.path.join(android_sdk, "platform-tools")


def main(argv: list[str] | None = None) -> int:
    """Main"""
    return trampoline(COMMAND, args=argv, default_path=DEFAULT_PATH)


if __name__ == "__main__":
    sys.exit(main())
