"""
Shared utility functions
"""

# pylint: disable=consider-using-with,global-statement,too-many-arguments,too-many-locals,fixme,too-many-statements,chained-comparison

import os
import sys

from pyflutterinstall.resources import (
    ANDROID_SDK,
    DOWNLOAD_DIR,
    FLUTTER_TARGET,
    INSTALL_DIR,
    JAVA_DIR,
)


def make_dirs() -> None:
    """Make directories for installation"""
    os.makedirs(INSTALL_DIR, exist_ok=True)
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    os.makedirs(ANDROID_SDK, exist_ok=True)
    os.makedirs(JAVA_DIR, exist_ok=True)

    INSTALL_DIR.mkdir(parents=True, exist_ok=True)
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    env = os.environ
    env[str(ANDROID_SDK)] = str(ANDROID_SDK)
    env[str(JAVA_DIR)] = str(JAVA_DIR)
    # add to path
    # ${FLUTTER_TARGET}/bin
    # add to path
    env["PATH"] = f"{FLUTTER_TARGET}/bin{os.pathsep}{env['PATH']}"
    env["PATH"] = f"{JAVA_DIR}/bin{os.pathsep}{env['PATH']}"


def make_title(title: str) -> None:
    """Make a title"""
    title = f" {title} "
    out = ""
    out += "\n\n###########################################\n"
    out += f"{title.center(43, '#')}\n"
    out += "###########################################\n\n\n"
    sys.stdout.write(out)
    sys.stdout.flush()


def print_tree_dir(path: str, max_level=2) -> None:
    """Prints the tree of a directory"""
    output = ""
    for root, dirs, files in os.walk(path):
        level = root.replace(path, "").count(os.sep)
        indent = " " * 4 * (level)
        if max_level > 0 and (level + 1) > max_level:
            del dirs[:]
            continue
        output += f"{indent}{os.path.basename(root)}" + os.linesep
        subindent = " " * 4 * (level + 1)
        for file in files:
            output += f"{subindent}{file}" + os.linesep
    sys.stdout.write(output)
    sys.stdout.flush()
