import sys
import urllib.parse as parse
from http.server import BaseHTTPRequestHandler

import requests

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.errors import SymAPIRequestError
from sym.flow.cli.helpers.config import Config
from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.jwt import JWT
from sym.flow.cli.models import AuthToken, Organization


def make_auth0_callback_handler(
    options: GlobalOptions, redirect_uri: str, state: str, code_verifier: str, organization: Organization
):
    """A Method that returns an HTTPRequestHandler class that can be passed into an HTTPServer instantiation.

    Handles a GET request callback from Auth0 after a user logs in:
    - Redirects the user to /cli/error if any errors occur (e.g. Invalid state parameter)
    - Exchanges the auth_code for an access token
    - Calls Queuer's VerifyLogin endpoint to validate that the user is a valid user in the organization.

    Note: The class has to be defined within this method because we can't change the shape of the __init__ method, as
    the handler is instantiated by the HTTPServer code upon each request (We only pass in the class type of the handler
    when we start the HTTPServer, not an instance of the handler). However, these values are needed to exchange the
    auth code and verify the login, so the class definition will reference the values passed in from this wrapper method
    and the wrapper will return the class reference that can be passed into HTTPServer.

    Args:
        options: A GlobalOptions instance that can be used to call the Queuer API
        redirect_uri: The redirect_uri parameter sent to Auth0 in the initial login URL
        state: The state parameter sent to Auth0 in the initial login URL
        code_verifier: The plaintext string used to generate the code_challenge sent to Auth0 in the initial login URL
        organization: The User's Organization
    """

    class Auth0HTTPRequestHandler(BaseHTTPRequestHandler):
        """A HTTPRequestHandler that handles the OAuth2.0 callback from Auth0 when a user logs in.
        See: https://auth0.com/docs/get-started/authentication-and-authorization-flow/authorization-code-flow-with-proof-key-for-code-exchange-pkce
        """

        def log_message(self, format, *args):
            """BaseHTTPRequestHandler will log requests and other messages to stderr. Override log_message to prevent
            any unnecessary prints to the CLI.
            """

        def do_GET(self):
            """Handles the callback from Auth0 after a user logs in on their browser."""
            parsed = parse.urlparse(self.path)

            # Checks if Auth0 returned any error messages and exits with an error if so.
            # Validates that both 'code' and 'state' parameters exists. Also validates that the state parameter
            # matches the state parameter generated at the beginning of the login process.
            code = self._validate_callback_params(parsed.query)

            # We're guaranteed to have an auth code at this point that we can exchange for an access token.
            auth_token = self._get_token_from_code(code)

            # Set the access token in GlobalOptions so that we can make API calls to Queuer
            options.set_access_token(auth_token.access_token)

            # Call Queuer's ValidateLogin API to verify that the user is a valid user in the Organization
            # (At this point we only know that they have a valid Auth0 login.)
            self._validate_login(auth_token)

            # Print success to the CLI, and redirect the browser to the Login Success page.
            cli_output.success("Login succeeded")
            self.send_response(301)
            self.send_header("Location", "https://static.symops.com/cli/login")
            self.end_headers()

        def _validate_callback_params(self, query: str):
            """
            Validates the callback query parameters. If:
                - An error_description exists
                - The `code` parameter is missing
                - The `state` parameter is missing, or doesn't match the state parameter we generated
            then the error is reported in both the browser and CLI. Then exits the CLI with exit code 1.

            Args:
                query: The query parameters passed into the GET request.

            Returns:
                The auth code from Auth0 (i.e. the 'code' parameter)
            """
            qs = parse.parse_qs(query)

            error_message = None
            if qs.get("error_description"):
                error_message = qs["error_description"][0]
            elif not qs.get("code"):
                error_message = "Missing code in query"
            elif not qs.get("state"):
                error_message = "Missing state in query"
            elif not qs["state"][0] == state:
                options.dprint(f"Invalid state. Found: {qs['state'][0]}, expected: {state}.")
                error_message = "Invalid state"

            # Redirect the browser with the error page and print the error to the CLI
            if error_message:
                self._exit_with_error(error_message)

            return qs["code"][0]

        def _exit_with_error(self, error_message: str):
            """Redirects the browser to the /cli/error page with the given error message, prints it to the CLI, then
            exits with an error code.
            """

            query = parse.urlencode({"message": error_message})
            self.send_response(301)
            self.send_header("Location", f"https://static.symops.com/cli/error?{query}")
            self.end_headers()

            if "complete sign up" in error_message:
                # If we know the problem is that the user just signed up (and therefore their email is not validated),
                # give them an info message telling them to verify their email.
                cli_output.info(error_message)
                sys.exit(0)
            else:
                # Otherwise, raise the error message that we got from the HTTP response.
                cli_output.fail(error_message)

        def _get_token_from_code(self, auth_code: str) -> AuthToken:
            """With the provided auth code and the initial code verifier, exchanges the auth code for an Auth0
            access token.
            See: https://auth0.com/docs/get-started/authentication-and-authorization-flow/authorization-code-flow-with-proof-key-for-code-exchange-pkce
            """
            data = {
                "grant_type": "authorization_code",
                "client_id": organization.client_id,
                "code_verifier": code_verifier,
                "code": auth_code,
                "redirect_uri": redirect_uri,
            }
            headers = {"content-type": "application/x-www-form-urlencoded"}
            url = f"{options.auth_url}/oauth/token"
            r = requests.post(url, headers=headers, data=data)
            if not r.ok:
                self._exit_with_error(
                    f"An unexpected error occurred while logging in, please try again later. {r.text}"
                )

            auth_token = AuthToken.parse_obj(r.json())
            return auth_token

        def _validate_login(self, auth_token: AuthToken):
            """Makes an API Call to Queuer to verify that the user that just logged in is a valid admin in the
            Organization. If not, then reports that error to the browser/CLI and exits.

            Args:
                auth_token: The AuthToken object received from a successful Auth0 login
            """

            jwt = JWT.from_access_token(auth_token.access_token, auth_url=options.auth_url)

            # Verify user exists in the organization
            try:
                # Check the User's session with the Sym API. This will validate that the JWT is still valid,
                # and matches the email address that the User is logged in with.
                user_data = options.sym_api.verify_login(segment_track=True)
            except SymAPIRequestError:
                self._exit_with_error("A server error has occurred, please try again later.")

            if user_data.get("error") and user_data.get("message"):
                self._exit_with_error(user_data["message"])
            elif user_data.get("error"):
                # All Sym API errors should have a message field, but just in case...
                self._exit_with_error(f"{jwt.email} is not a valid user in the Organization {organization.slug}")

            # We successfully validated the user. Save the access token to the symflow config
            Config.store_login_config(jwt.email, organization, auth_token)

    return Auth0HTTPRequestHandler
