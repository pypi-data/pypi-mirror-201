"""
Contains the install functions for the various components
"""

# pylint: disable=missing-function-docstring,consider-using-with,disable=invalid-name,subprocess-run-check,line-too-long,R0801

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

from download import download  # type: ignore

from pyflutterinstall.resources import (
    DOWNLOAD_DIR,
    INSTALL_DIR,
    JAVA_DIR,
    get_platform_java_sdk,
    JAVA_SDK_VERSIONS,
)
from pyflutterinstall.setenv import add_env_path, set_env_var
from pyflutterinstall.util import make_title


def install_java_sdk(version: int = 11) -> int:
    make_title("Installing Java SDK")
    java_sdk_url = get_platform_java_sdk(version)
    print(f"Install Java SDK from {java_sdk_url} to {INSTALL_DIR}")
    java_sdk_zip_file = Path(
        download(java_sdk_url, DOWNLOAD_DIR / os.path.basename(java_sdk_url))
    )
    if os.path.exists(JAVA_DIR):
        print(f"Removing existing Java SDK at {JAVA_DIR}")
        shutil.rmtree(JAVA_DIR)
    print(f"Unpacking {java_sdk_zip_file} to {JAVA_DIR}")
    shutil.unpack_archive(java_sdk_zip_file, JAVA_DIR)
    base_java_dir = JAVA_DIR / os.listdir(JAVA_DIR)[0]
    print(base_java_dir)
    if sys.platform == "darwin":
        java_bin_dir = base_java_dir / "Contents" / "Home" / "bin"
    else:
        java_bin_dir = base_java_dir / "bin"
    # check that java is in the path
    print(java_bin_dir)
    java_exe = "java.exe" if os.name == "nt" else "java"
    assert java_exe in os.listdir(java_bin_dir), "java not found in java bin dir"
    add_env_path(java_bin_dir)
    if sys.platform == "darwin":
        set_env_var("JAVA_HOME", str(base_java_dir / "Contents" / "Home"))
    else:
        set_env_var("JAVA_HOME", str(base_java_dir))
    found_java_path = shutil.which("java")
    assert found_java_path is not None, "No java path found"
    assert (
        str(java_bin_dir) in found_java_path
    ), f"java installed not in expected path, instead it's {found_java_path}"
    java_version = subprocess.check_output(
        "java -version", shell=True, universal_newlines=True, stderr=subprocess.STDOUT
    )
    print(f"Java SDK installed: {java_version}\n")
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version",
        type=int,
        default=11,
        help="The version of Java to install",
        choices=JAVA_SDK_VERSIONS.keys(),
    )
    args = parser.parse_args()
    install_java_sdk(args.version)


if __name__ == "__main__":
    main()
