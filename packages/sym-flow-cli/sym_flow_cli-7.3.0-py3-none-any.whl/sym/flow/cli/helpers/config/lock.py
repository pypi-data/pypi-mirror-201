import os
from pathlib import Path

from portalocker import Lock
from portalocker.constants import LOCK_EX, LOCK_NB, LOCK_SH

""" 
    For a refresher on file-opening modes:
     `r`   Open text file for reading.  The stream is positioned at the
             beginning of the file.
    
     `r+`  Open for reading and writing.  The stream is positioned at the
             beginning of the file.
"""


def read_lock(path: Path):
    """
    Returns a Portalocker Read Lock for the file specified at `path`.
    Treat this method like the `open(filename, 'r')` Python method.

    Args:
        path: The path to the file (e.g. Path("~/.config/symflow/default/config.yml")
    """

    return Lock(
        str(path),
        # read-only mode
        mode="r",
        # LOCK_SH = Place a shared lock. More than one process may hold a shared lock for a given file at a given time
        # LOCK_NB = Acquire the lock in a non-blocking fashion
        flags=LOCK_SH | LOCK_NB,
        # Create the file on open if it doesn't exist.
        opener=lambda path, flags: os.open(path, flags | os.O_CREAT),
    )


def read_write_lock(path: Path):
    """
    Returns a Portalocker Read-Write Lock (r+) for the file specified at `path`.
    If the file doesn't exist yet, creates the file first.
    Treat this method like the `open(filename, 'r+')` Python method.

    This is a "spinlock" (https://en.wikipedia.org/wiki/Spinlock)

    Args:
        path:The path to the file (e.g. Path("~/.config/symflow/default/config.yml")
    """

    return Lock(
        str(path),
        # Read/write mode
        mode="r+",
        # LOCK_EX = exclusive lock. Only one process may hold an exclusive lock at a time
        # LOCK_NB = Acquire the lock in a non-blocking fashion
        flags=LOCK_EX | LOCK_NB,
        # Create the file on open if it doesn't exist.
        opener=lambda path, flags: os.open(path, flags | os.O_CREAT),
    )
