"""
Contains the install functions for the various components
"""

# pylint: disable=missing-function-docstring,consider-using-with,disable=invalid-name,subprocess-run-check,line-too-long

import argparse
import os
import shutil
import sys

from download import download  # type: ignore
from shellexecute import execute  # type: ignore

from pyflutterinstall.resources import (
    ANDROID_SDK,
    ANDROID_SDK_URL,
    CMDLINE_TOOLS,
    DOWNLOAD_DIR,
    INSTALL_DIR,
    IS_GITHUB_RUNNER,
)
from pyflutterinstall.setenv import add_env_path, set_env_var
from pyflutterinstall.util import make_title


def install_android_sdk(prompt: bool) -> int:
    make_title("Installing Android SDK")
    print(
        f"Install Android commandline-tools SDK from {ANDROID_SDK_URL} to {INSTALL_DIR}"
    )
    # sdk\Android\tools\bin\sdkmanager.bat
    path = download(ANDROID_SDK_URL, DOWNLOAD_DIR / os.path.basename(ANDROID_SDK_URL))
    print(f"Unpacking {path} to {INSTALL_DIR}")
    shutil.unpack_archive(path, ANDROID_SDK / "cmdline-tools" / "tools")
    sdkmanager_name = "sdkmanager.bat" if os.name == "nt" else "sdkmanager"
    sdkmanager_path = (
        ANDROID_SDK
        / "cmdline-tools"
        / "tools"
        / "cmdline-tools"
        / "bin"
        / sdkmanager_name
    )
    if not os.path.exists(sdkmanager_path):
        raise FileNotFoundError(f"Could not find {sdkmanager_path}")
    os.chmod(sdkmanager_path, 0o755)
    # Adding the sdkmanager shouldn't be needed because it should be installed to
    # latest.
    # add_env_path(sdkmanager_path.parent)
    print("About to install Android SDK tools")
    # install latest
    execute(
        f'{sdkmanager_path} --sdk_root="{ANDROID_SDK}" --install "platform-tools"',
        send_confirmation=[("Accept? (y/N):", "y")] if not prompt else None,
        ignore_errors=False,
    )
    set_env_var("ANDROID_SDK_ROOT", ANDROID_SDK)
    set_env_var("ANDROID_HOME", ANDROID_SDK)
    # update tools
    print(f"Updating Android SDK with {sdkmanager_path}")
    execute(
        f'{sdkmanager_path} --sdk_root="{ANDROID_SDK}" --update',
        send_confirmation=[("Accept? (y/N):", "y")] if not prompt else None,
        ignore_errors=False,
    )
    tools_to_install = [f'"{tool}"' for tool in CMDLINE_TOOLS]
    for tool in tools_to_install:
        execute(
            f'{sdkmanager_path} --sdk_root="{ANDROID_SDK}" --verbose --install {tool}',
            send_confirmation=[("Accept? (y/N):", "y")] if not prompt else None,
            ignore_errors=False,
            timeout=60 * 20,
        )
    confirmation = "y\ny\ny\ny\ny\ny\ny\ny\ny\ny\ny\ny\nn\n"
    send_confirmation = []
    send_confirmation.append(
        ("Review licenses that have not been accepted (y/N)?", "y")
    )
    for conf in confirmation.splitlines():
        send_confirmation.append(("Accept? (y/N):", conf))
    execute(
        f'{sdkmanager_path} --licenses --sdk_root="{ANDROID_SDK}"',
        send_confirmation=send_confirmation if not prompt else None,
        ignore_errors=False,
    )
    add_env_path(ANDROID_SDK / "platform-tools")
    add_env_path(ANDROID_SDK / "emulator")
    add_env_path(ANDROID_SDK / "tools" / "bin")
    # avdmanager needs to get picked up from here.
    add_env_path(ANDROID_SDK / "cmdline-tools" / "latest" / "bin")
    if sys.platform == "darwin":
        if IS_GITHUB_RUNNER:
            package_mgr = "gem"
        else:
            package_mgr = "brew"
        execute(f"{package_mgr} install cocoapods", ignore_errors=True)
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", action="store_true")
    args = parser.parse_args()
    install_android_sdk(args.prompt)


if __name__ == "__main__":
    print("blah")
    sys.exit(main())
