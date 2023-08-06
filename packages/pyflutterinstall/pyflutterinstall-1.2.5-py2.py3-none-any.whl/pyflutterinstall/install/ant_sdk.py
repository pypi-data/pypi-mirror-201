"""
Contains the install functions for the various components
"""

# pylint: disable=missing-function-docstring,consider-using-with,disable=invalid-name,subprocess-run-check,line-too-long

import os
import shutil
import sys
from pathlib import Path

from download import download  # type: ignore
from shellexecute import execute  # type: ignore

from pyflutterinstall.resources import (
    ANT_DIR,
    ANT_SDK_DOWNLOAD,
    DOWNLOAD_DIR,
    INSTALL_DIR,
)
from pyflutterinstall.setenv import add_env_path
from pyflutterinstall.util import make_title


def install_ant_sdk() -> int:
    make_title("Installing Ant SDK")
    if sys.platform in ["win32", "linux"]:
        print(f"Install Ant from {ANT_SDK_DOWNLOAD} to {INSTALL_DIR}")
        ant_sdk_sip = Path(
            download(
                ANT_SDK_DOWNLOAD, DOWNLOAD_DIR / os.path.basename(ANT_SDK_DOWNLOAD)
            )
        )
        if os.path.exists(ANT_DIR):
            print(f"Removing existing Ant SDK at {ANT_DIR}")
            shutil.rmtree(ANT_DIR)
        print(f"Unpacking {ant_sdk_sip} to {ANT_DIR}")
        shutil.unpack_archive(ant_sdk_sip, ANT_DIR)
        base_ant_dir = ANT_DIR / os.listdir(ANT_DIR)[0]
        print(base_ant_dir)
        ant_bin_dir = base_ant_dir / "bin"
        add_env_path(ant_bin_dir)
        # check that ant is in the path
        print(f"Ant SDK installed: {base_ant_dir}\n")
    if sys.platform == "darwin":
        execute("brew install ant")
    assert shutil.which("ant"), "ant not found in ant bin dir"
    return 0


def main():
    install_ant_sdk()


if __name__ == "__main__":
    sys.exit(main())
