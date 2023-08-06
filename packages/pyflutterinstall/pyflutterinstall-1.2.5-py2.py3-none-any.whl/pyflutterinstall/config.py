"""
Saves the global runtime configuration of the install state.
"""
import json
import os

from appdirs import user_config_dir  # type: ignore

CONFIG_DIR = user_config_dir("pyflutterinstall")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")


def config_save(config: dict):
    """Dumps the json to disk."""
    out_content = json.dumps(config, indent=4)
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, encoding="utf-8", mode="w") as filed:
        filed.write(out_content)


def config_load() -> dict:
    """Loads the json from disk."""
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, encoding="utf-8", mode="r") as filed:
        return json.load(filed)


def print_config() -> int:
    """Endpoint for printing the current configuration."""
    config = config_load()
    print(json.dumps(config, indent=4))
    return 0
