from contextlib import contextmanager
from typing import Any, Optional

import yaml
from pydantic import BaseModel

from sym.flow.cli.helpers.utils import filter_dict
from sym.flow.cli.models import AuthToken, Organization

from .thread_safe_file import ThreadSafeFile


class ConfigFile(BaseModel):
    """A Pydantic model representing the contents of ~/.config/symflow/default/config.yml"""

    org: Optional[str] = None
    client_id: Optional[str] = None
    email: Optional[str] = None
    auth_token: Optional[AuthToken] = None

    @property
    def access_token(self) -> Optional[str]:
        if self.auth_token:
            return self.auth_token.access_token
        return None

    def deepget(self, key: str) -> Optional[Any]:
        """Tries to get a nested attribute from the config file (e.g. "auth_token.access_token")"""
        data = self
        for k in key.split("."):
            try:
                data = getattr(data, k)
            except AttributeError:
                return None

        return data


class Config:
    """A singleton class providing helper methods for accessing and modifying the symflow config file."""

    def __init__(self) -> None:
        self.file = ThreadSafeFile(path=(ThreadSafeFile.xdg_config_home() / "symflow/default/config.yml"))

        # Analogous to Python's built-in `with open(file)`, but with the locking mechanisms provided by ThreadSafeFile.
        with self.file.read() as f:
            # Initialize `self.config` with the config file from the file system.
            self.__load(f)

    @classmethod
    def reset(cls):
        """Replaces the singleton instance of this class with a new instance."""
        setattr(cls, "__instance", cls())

    @classmethod
    def instance(cls) -> "Config":
        """Returns a singleton instance of this class."""
        if not hasattr(Config, "__instance"):
            # If no instance exists yet, generate a new one
            Config.reset()

        # Return the existing instance
        return getattr(Config, "__instance")

    def __load(self, file_stream):
        """Loads the config file from the given file-stream into memory as a Pydantic model set as an attribute on the
        Singleton instance,"""
        self.config = ConfigFile(**(yaml.safe_load(stream=file_stream) or {}))

    def __flush(self, file_stream):
        """Writes the in-memory Pydantic model ConfigFile to the file-stream."""
        file_stream.seek(0)
        file_stream.truncate()
        yaml.safe_dump(filter_dict(self.config.dict()), stream=file_stream)

    @contextmanager
    def atomic(self):
        """A context manager that locks the config file for atomic updates."""

        # Analogous to Python's built-in `with open(file, 'r+')`,
        # but with the locking mechanisms provided by ThreadSafeFile.
        with self.file.update() as f:
            # Refresh the in-memory file from the file system.
            self.__load(f)
            yield
            # Write the new values to the system.
            self.__flush(f)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({str(self.file)})"

    @classmethod
    def get_value(cls, key: str) -> Optional[str]:
        """Given a dot-separated string, attempts to get that attribute from the config.
        If the attribute doesn't exist, returns None.
        (e.g. key = "auth_token.access_token")
        """
        config = cls.instance().config
        return config.deepget(key)

    @classmethod
    def set_email(cls, email: str):
        config_manager = cls.instance()
        with config_manager.atomic():
            config = config_manager.config
            config.email = email

    @classmethod
    def get_email(cls) -> Optional[str]:
        return cls.instance().config.email

    @classmethod
    def set_auth_token(cls, auth_token: AuthToken):
        config_manager = cls.instance()
        with config_manager.atomic():
            config = config_manager.config
            config.auth_token = auth_token

    @classmethod
    def get_org(cls) -> Optional[Organization]:
        """Returns an Organization object containing the Org slug and Auth0 Client ID, if exists."""
        config = cls.instance().config
        if config.org:
            return Organization(slug=config.org, client_id=config.client_id)

        return None

    @classmethod
    def get_org_slug(cls) -> Optional[str]:
        """Returns the Org slug set in the config, if exists."""
        config = cls.instance().config
        return config.org

    @classmethod
    def set_org(cls, org: Organization):
        """Sets the org slug and Auth0 Client ID in the config file."""
        config_manager = cls.instance()
        with config_manager.atomic():
            config = config_manager.config
            config.org = org.slug
            config.client_id = org.client_id

    @classmethod
    def get_access_token(cls) -> Optional[str]:
        """Returns the Auth0 access token stored under `auth_token.access_token`"""
        return cls.instance().config.access_token

    @classmethod
    def is_logged_in(cls) -> bool:
        """Returns a boolean indicating if the user is logged in (i.e. has an auth_token set)."""
        return cls.instance().config.auth_token is not None

    @classmethod
    def logout(cls):
        """Logs out of symflow by removing the user's email and auth_token from the config file."""
        if not cls.is_logged_in():
            return

        config_manager = cls.instance()
        with config_manager.atomic():
            config = config_manager.config
            config.email = None
            config.auth_token = None

    @classmethod
    def store_login_config(cls, email: str, org: Organization, auth_token: AuthToken) -> str:
        """Updates the entire config file with the given values."""
        cls.set_org(org)
        cls.set_email(email)
        cls.set_auth_token(auth_token)
        return str(cls.instance().file)
