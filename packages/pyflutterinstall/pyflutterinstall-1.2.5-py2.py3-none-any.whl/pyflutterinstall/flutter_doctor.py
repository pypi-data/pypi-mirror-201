"""
Contains the install functions for the various components
"""

# pylint: disable=missing-function-docstring,consider-using-with,disable=invalid-name,subprocess-run-check,line-too-long

import shutil

from shellexecute import execute  # type: ignore

from pyflutterinstall.util import make_title


def postinstall_run_flutter_doctor() -> None:
    cmd = "flutter doctor -v"
    make_title(f"Executing '{cmd}'")
    if not shutil.which("flutter"):
        print("Flutter not found in path")
        return
    execute(cmd, ignore_errors=False)
