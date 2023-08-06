"""
Command stub for sdkmanager
"""

import sys
import os
import warnings

from pyflutterinstall.config import config_load
from pyflutterinstall.trampoline import trampoline

COMMAND = "gradle"


def get_gradle_path() -> str | None:
    """Get gradle path"""
    install_dir = config_load().get("INSTALL_DIR")
    if install_dir is None:
        warnings.warn("INSTALL_DIR not set")
        return None
    gradle_base_directory = os.path.join(install_dir, "gradle")

    dirs = os.listdir(gradle_base_directory)
    if not dirs:
        return None
    if len(dirs) > 1:
        dirs.sort()
        dirs.reverse()
        warnings.warn("Multiple gradle versions found, using the latest one")
    fulldirs = [os.path.join(gradle_base_directory, d) for d in dirs]
    return os.path.join(fulldirs[0], "bin")


def main(argv: list[str] | None = None) -> int:
    """Main"""
    return trampoline(COMMAND, args=argv, default_path=get_gradle_path())


if __name__ == "__main__":
    sys.exit(main())
