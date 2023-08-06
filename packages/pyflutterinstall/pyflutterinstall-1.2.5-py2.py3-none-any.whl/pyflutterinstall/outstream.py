"""
Oustream.
"""

# pylint: disable=no-self-argument,no-method-argument

import sys
from typing import Optional


class Outstream:
    """Outstream for pexpect"""

    def __init__(self) -> None:
        self.buffer = ""

    def write(self, data: Optional[str] = None) -> None:
        """Writes to the buffer."""
        if data is None:
            return
        self.buffer += data
        sys.stdout.write(data)

    def flush() -> None:  # type: ignore
        """Flushes the buffer."""
        sys.stdout.flush()
