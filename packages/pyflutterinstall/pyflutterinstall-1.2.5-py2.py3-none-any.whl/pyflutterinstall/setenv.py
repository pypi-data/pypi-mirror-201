"""
This module provides functions for setting environment variables.
"""

# pylint: disable=import-outside-toplevel

import os
from pathlib import Path
from typing import Union

import setenvironment  # type: ignore
from dotenv import get_key, load_dotenv, set_key

ENV_FILE = "./.env"
INITIALIZED = False


def uniquify_paths(paths: list[str]) -> list[str]:
    """Removes duplicate paths from the given path string."""
    found = set()
    result = []
    for path in paths:
        if path not in found:
            result.append(path)
            found.add(path)
    return result


def init_dotenv() -> None:
    """Initializes the dotenv environment."""
    global INITIALIZED  # pylint: disable=global-statement
    if INITIALIZED:
        return
    INITIALIZED = True
    load_dotenv(ENV_FILE, override=True)
    flutter_paths = get_key(ENV_FILE, "FLUTTER_PATHS")
    print(f"*** FLUTTER_PATHS: {flutter_paths}")
    if flutter_paths is not None:
        paths = flutter_paths.split(os.pathsep)
        if paths:
            os_env_paths = os.environ.get("PATH", "").split(os.pathsep)
            paths = paths + os_env_paths
            paths = uniquify_paths(paths)
            os.environ["PATH"] = os.pathsep.join(paths)


init_dotenv()


def set_env_var(var_name: str, var_value: Union[str, Path], verbose=True):
    """Sets an environment variable for the platform."""
    var_value = str(var_value)
    set_key(ENV_FILE, var_name, var_value)
    if verbose:
        print(f"$$$ Setting {var_name} to {var_value}")
    setenvironment.set_env_var(var_name, var_value)


def add_env_path(new_path: Union[Path, str]):
    """Adds a path to the front of the PATH environment variable."""
    new_path = str(new_path)
    env_path = get_key(ENV_FILE, "FLUTTER_PATHS") or ""
    if new_path not in env_path:
        if not env_path:
            env_path = new_path
        else:
            env_path = env_path + os.pathsep + new_path
        set_key(ENV_FILE, "FLUTTER_PATHS", env_path)
    else:
        env_path = new_path
    setenvironment.add_env_path(new_path)


def get_env_path() -> str:
    """Gets the PATH environment variable."""
    return setenvironment.get_env_var("PATH")


def get_env_var(var_name: str) -> str:
    """Gets an environment variable."""
    return setenvironment.get_env_var(var_name)
