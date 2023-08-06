import uuid
import webbrowser
from abc import ABC, abstractmethod
from http.server import HTTPServer
from typing import Optional, Tuple

import click
import pkce
import requests

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.errors import LoginError
from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.login.handler import make_auth0_callback_handler
from sym.flow.cli.models import AuthToken, Organization


class LoginFlow(ABC):
    @abstractmethod
    def login(self, options: GlobalOptions, org: Organization) -> AuthToken:
        pass


class BrowserRedirectFlow(LoginFlow):
    """
    Issue an authorization code request by opening the browser to a particular
    URL. Start a server and wait for the user to successfully login. The browser will
    redirect a successful login back to the locally running server, with a request
    body containing an auth code. With the auth code, obtain an access token.

    Implements the auth code flow described here:
    https://www.altostra.com/blog/cli-authentication-with-auth0
    """

    def __init__(self, port: int):
        self.port: int = port
        self.redirect_url: str = f"http://localhost:{self.port}/callback"

        # Tuple of: url, state, code_verifier
        self.browser_login_params: Optional[Tuple[str, str, str]] = None

    def login(self, options: GlobalOptions, org: Organization):
        # Generate the Auth0 login URL
        (url, state, code_verifier) = self.gen_browser_login_params(options, org)

        # Print a copiable URL to the CLI
        styled_url = click.style(requests.utils.requote_uri(url), bold=True)  # type: ignore
        cli_output.info(
            f"Opening the login page in your browser. If this doesn't work, please visit the following URL:\n"
            f"{styled_url}\n"
        )

        # Start the HTTPServer that will listen for the callback after the user logs in.
        handler = make_auth0_callback_handler(options, self.redirect_url, state, code_verifier, org)
        with self._login_callback_server(handler) as httpd:
            # Open the URL in the user's browser.
            webbrowser.open(url)

            # Block and wait for the callback
            httpd.handle_request()

    def _login_callback_server(self, handler):
        """Starts an HTTPServer on the given port that will handle the callback from Auth0 after a user logs in on
        their browser.
        """
        try:
            return HTTPServer(("localhost", self.port), handler)
        except OSError as e:
            if e.errno in (48, 98):  # Address already in use
                raise LoginError(
                    f"Port {self.port} is already taken.",
                    "Try running `symflow login --port <port_number>` with an unused port.",
                )

    def gen_browser_login_params(
        self, options: GlobalOptions, org: Organization, force: bool = False
    ) -> Tuple[str, str, str]:
        """Generates the initial login URL that directs the user to log into Auth0."""

        if force or self.browser_login_params is None:
            state = str(uuid.uuid4())
            code_verifier = pkce.generate_code_verifier(length=128)
            code_challenge = pkce.get_code_challenge(code_verifier)
            query_params = "&".join(
                [
                    "response_type=code",
                    f"client_id={org.client_id}",
                    "code_challenge_method=S256",
                    f"code_challenge={code_challenge}",
                    f"redirect_uri={self.redirect_url}",
                    f"audience=https://api.symops.com",
                    f"state={state}",
                    "scope=login:cli",
                    "prompt=login",
                ]
            )
            url = f"{options.auth_url}/authorize?{query_params}"
            self.browser_login_params = (url, state, code_verifier)

        return self.browser_login_params
