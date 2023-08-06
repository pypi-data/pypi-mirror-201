"""
Command stub for sdkmanager
"""
import os
import sys
from pyflutterinstall.trampoline import trampoline
from pyflutterinstall.config import config_load

ANDROID_SDK = config_load().get("ANDROID_SDK", ".")
if ANDROID_SDK != ".":
    os.environ["ANDROID_SDK"] = ANDROID_SDK
    os.environ["ANDROID_HOME"] = ANDROID_SDK

COMMAND = "sdkmanager"
DEFAULT_PATH = os.path.join(ANDROID_SDK, "cmdline-tools", "latest", "bin")


def main(argv: list[str] | None = None) -> int:
    """Main"""
    return trampoline(COMMAND, args=argv, default_path=DEFAULT_PATH)


if __name__ == "__main__":
    sys.exit(main())
