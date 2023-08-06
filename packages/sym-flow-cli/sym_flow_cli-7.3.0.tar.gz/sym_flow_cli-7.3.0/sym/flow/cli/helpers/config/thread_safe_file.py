import os
from contextlib import contextmanager
from pathlib import Path

from .lock import read_lock, read_write_lock


class ThreadSafeFile:
    """A class that provides read/write access to a File protected by portalocker Locks
    https://portalocker.readthedocs.io/en/latest/index.html
    """

    def __init__(self, path: Path):
        # Make the path absolute, resolving all symlinks on the way and also normalizing it
        self.path = path.resolve()
        self.mkparents()

        # Create locking mechanisms for the given file
        self.read_lock = read_lock(self.path)
        self.update_lock = read_write_lock(self.path)

    def __str__(self):
        return str(self.path)

    @classmethod
    def xdg_config_home(cls) -> Path:
        """Returns the path to the .config directory.
        If the XDG_CONFIG_HOME envvar is set, uses that as the config directory.
        Otherwise, the .config directory defaults to ~/.config

        XDG Base Directory Specification Basics:
        https://specifications.freedesktop.org/basedir-spec/latest/ar01s02.html
        """
        try:
            return Path(os.environ["XDG_CONFIG_HOME"]).expanduser().resolve()
        except KeyError:
            return Path.home() / ".config"

    def mkparents(self):
        """Creates all the parent directories for the config file if they don't exist."""
        self.path.parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def read(self):
        """Reads the given string from the file."""
        with self.read_lock as f:
            f.seek(0)  # Start cursor at the beginning of the file
            yield f

    @contextmanager
    def update(self):
        """Grabs a read-write lock on the config file for the duration of the context"""
        self.mkparents()
        with self.update_lock as f:
            f.seek(0)  # Start cursor at the beginning of the file
            yield f
