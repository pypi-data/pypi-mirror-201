"""
Contains the install functions for the various components
"""

# pylint: disable=missing-function-docstring,consider-using-with,disable=invalid-name,subprocess-run-check,line-too-long,R0801

import argparse
import os
import shutil

from shellexecute import execute  # type: ignore

from pyflutterinstall.resources import ANDROID_SDK, FLUTTER_GIT_DOWNLOAD, FLUTTER_TARGET
from pyflutterinstall.setenv import add_env_path
from pyflutterinstall.util import make_title


def install_flutter_sdk(prompt: bool, install_precache=False) -> int:
    make_title("Installing Flutter")
    if shutil.which("git") is None:
        error_msg = "'git' not found in path"
        error_msg += "\npath = \n"
        for path in os.environ["PATH"].split(os.path.pathsep):
            error_msg += f"  {path}\n"
        print(error_msg)
        raise FileNotFoundError(error_msg)
    print(f"Install Flutter from {FLUTTER_GIT_DOWNLOAD} to {FLUTTER_TARGET}")
    if not FLUTTER_TARGET.exists():
        cmd = f'{FLUTTER_GIT_DOWNLOAD} "{FLUTTER_TARGET}"'
        execute(cmd, ignore_errors=False)
    else:
        print(f"Flutter already installed at {FLUTTER_TARGET}")
    if not os.path.exists(FLUTTER_TARGET):
        print(
            f"!!!!!!!!!!!!! FLUTTER FOLDER {FLUTTER_TARGET} DOES NOT EXIST EITHER !!!!!!!!!!!!!!!"
        )
        path = os.environ["PATH"]
        error_msg = f"Could not find {FLUTTER_TARGET} in path"
        error_msg += "\npath = \n"
        for path in path.split(os.pathsep):
            error_msg += f"  {path}\n"
        print(error_msg)
        raise FileNotFoundError(error_msg)
    # Add flutter to path
    add_env_path(FLUTTER_TARGET / "bin")
    execute(
        f'flutter config --android-sdk "{ANDROID_SDK}" --no-analytics',
        send_confirmation=[("Accept? (y/n): ", "y")] if not prompt else None,
        ignore_errors=False,
        timeout=60 * 20,
    )
    confirmation = "y\ny\ny\ny\ny\ny\ny\ny\ny\ny\ny\ny\n"
    send_confirmation = [
        ("Accept? (y/n): ", conf.strip())
        for conf in confirmation.splitlines()
        if conf.strip()
    ]
    if install_precache:
        execute("flutter precache", ignore_errors=True)
    execute(
        "flutter doctor --android-licenses 2>&1",
        send_confirmation=send_confirmation if not prompt else None,
        ignore_errors=False,
        timeout=60 * 20,
    )
    # os.system("echo y | flutter doctor --android-licenses")
    print("Flutter installed.\n")
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", action="store_true")
    args = parser.parse_args()
    install_flutter_sdk(not args.prompt)


if __name__ == "__main__":
    main()
