"""
Contains the install functions for the various components
"""

# pylint: disable=missing-function-docstring,consider-using-with,disable=invalid-name,subprocess-run-check,line-too-long,R0801

import os
import subprocess

from download import download  # type: ignore

from pyflutterinstall.resources import CHROME_URL, DOWNLOAD_DIR, INSTALL_DIR
from pyflutterinstall.util import make_title


def install_chrome() -> int:
    make_title("Installing Chrome")
    # Install chrome for windows
    try:
        stdout = subprocess.check_output(
            "flutter doctor",
            shell=True,
            text=True,
            encoding="utf-8",
            universal_newlines=True,
        )
        if "Cannot find Chrome" in stdout:
            print("Chrome not found, installing")
            print(f"Install Chrome from {CHROME_URL} to {INSTALL_DIR}")
            path = download(CHROME_URL, DOWNLOAD_DIR / os.path.basename(CHROME_URL))
            print(f"Downloaded chrome at {path}")
            # install it
            os.system(f'"{path}"')
    except subprocess.CalledProcessError as exc:
        print(
            f"Error while installing chrome:\n  status={exc.returncode},\n  output={exc.output}"
        )
    return 0


def main():
    install_chrome()


if __name__ == "__main__":
    main()
