import inspect
import logging
from dataclasses import dataclass
from typing import Optional, Sequence
from urllib.parse import urlparse

from sym.flow.cli.helpers.constants import DEFAULT_API_URL, DEFAULT_AUTH_URL


@dataclass
class GlobalOptions:
    api_url: str = DEFAULT_API_URL
    auth_url: str = DEFAULT_AUTH_URL
    access_token: Optional[str] = None
    debug: bool = False

    def dprint(self, *s: Sequence[str], **kwargs):
        """Prints debug messages if `self.debug` is True"""

        s = list(map(str, filter(None, s)))
        if (s or kwargs) and self.debug:
            message = " ".join(s)
            if kwargs:
                message += ": " + ",".join([f"{k}={v}" for k, v in kwargs.items()])
            mod = inspect.getmodule(inspect.stack()[1][0])
            logging.getLogger(mod.__name__ if mod else __name__).info(message)

    @property
    def sym_api(self):
        from sym.flow.cli.helpers.api import SymAPI

        return SymAPI(self.api_url, self.access_token)

    def set_access_token(self, sym_jwt):
        self.access_token = sym_jwt.strip()

    def set_api_url(self, url):
        url = url.rstrip("/")
        if not self._validate_url(url):
            raise ValueError(f"Specified SYM_API_URL '{url}' is not valid.")

        self.api_url = url

    def set_auth_url(self, url):
        url = url.rstrip("/")
        if not self._validate_url(url):
            raise ValueError(f"Specified SYM_AUTH_URL '{url}' is not valid.")

        self.auth_url = url

    def _validate_url(self, url):
        """Validates that the given URL:
        - Is `http` or `https`
        - Has a domain (e.g. api.symops.com)
        - Has no fragment (i.e. the part of the URL after `#`)
        - Has no query parameters
        - Has no param (i.e. the part between the path and the query)

        Details about the different parts of a URL:
        https://stackoverflow.com/questions/53992694/what-does-netloc-mean
        """
        try:
            parts = urlparse(url)
            if parts.scheme not in ("http", "https"):
                return False
            if not parts.netloc:
                return False
            if parts.fragment or parts.query or parts.params:
                return False
            return True
        except ValueError:
            return False

    def to_dict(self):
        return {
            "debug": self.debug,
            "api_url": self.api_url,
            "auth_url": self.auth_url,
        }
