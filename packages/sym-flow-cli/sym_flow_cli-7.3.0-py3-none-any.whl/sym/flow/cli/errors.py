from typing import Dict, List, Optional, Union

import click
from click import ClickException

from sym.flow.cli.helpers.constants import SYM_SUPPORT_EMAIL


class CliErrorMeta(type):
    """A metaclass that gives a unique exit code for each CliError class"""

    _exit_code_count = 2

    def __new__(cls, name, bases, attrs):
        cls._exit_code_count += 1
        klass = super().__new__(cls, name, bases, attrs)
        klass.exit_code = cls._exit_code_count
        return klass


class CliError(ClickException, metaclass=CliErrorMeta):
    """A superclass for all custom errors raised by symflow CLI."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def format_message(self):
        """Styles the outputted error messages of this class as bolded red text."""
        return click.style(self.message, fg="red", bold=True)


class CliErrorWithHint(CliError):
    """A superclass for custom errors raised by symflow CLI that have additional hint text."""

    def __init__(self, message, hints, **kwargs) -> None:
        self.hints = hints if isinstance(hints, list) else [hints]
        super().__init__(message, **kwargs)

    def __str__(self):
        return "\n\n".join(
            [
                self.message,
                *[f"Hint: {hint}" for hint in self.hints],
            ]
        )

    def format_message(self):
        """Styles the outputted error message as bolded red text, and hints as bolded cyan text."""
        msg = click.style(self.message, fg="red", bold=True)
        styled = [click.style(hint, fg="cyan", bold=True) for hint in self.hints]
        hint = "\n\n" + "\n\n".join([f"Hint: {hint}" for hint in styled])
        return f"{msg}{hint}"


class UnexpectedError(CliError):
    def __init__(self, ex: str) -> None:
        super().__init__(f"An unexpected error occurred: {ex}")


class SSLConnectionError(CliError):
    def __init__(self, ex: str) -> None:
        super().__init__(
            f"{ex}. This is usually caused by network monitoring/limiting software on the local computer. "
            f"Try disabling it. If the issue persists, please contact {SYM_SUPPORT_EMAIL}."
        )


class LoginError(CliErrorWithHint):
    def __init__(self, error_message: str, hint: str) -> None:
        super().__init__(error_message, hint)


class UnknownOrgError(CliError):
    def __init__(self, org_id: str) -> None:
        super().__init__(f"Unknown organization with ID: {org_id}")


class UnknownUserError(CliError):
    def __init__(self, email: str) -> None:
        super().__init__(f"Unknown user for email: {email}")


class UnknownBotError(CliError):
    def __init__(self, username: str) -> None:
        super().__init__(f"Unknown bot: {username}")


class UserAlreadyExists(CliError):
    def __init__(self, email: str) -> None:
        super().__init__(f"A user already exists with email: {email}")


class BotAlreadyExists(CliError):
    def __init__(self, username: str) -> None:
        super().__init__(f"A bot already exists with username: {username}")


class NotLoggedInError(CliErrorWithHint):
    def __init__(self) -> None:
        super().__init__(
            "You must be logged in to perform this action.",
            "Run `symflow login` to log in.",
        )


class MissingServiceError(CliErrorWithHint):
    def __init__(self, service_type: str) -> None:
        super().__init__(
            f"No service is registered for type {service_type}",
            f"You can create the service by declaring a `sym_integration` resource with `type={service_type}` in your Terraform configuration",
        )


class MissingIdentityValueError(CliErrorWithHint):
    def __init__(self, identifier: str, command: str = "users") -> None:
        super().__init__(
            "Identity value cannot be empty",
            f"If you want to delete the identity, run `symflow {command} delete-identity {identifier}`",
        )


class InvalidChoiceError(CliErrorWithHint):
    def __init__(self, value: str, valid_choices: List[str]) -> None:
        super().__init__(
            f"Invalid input: '{value}'",
            f"Try one of: {', '.join(valid_choices)}",
        )


class MissingChoicesError(CliError):
    def __init__(self) -> None:
        super().__init__("No choices were provided!")


class ReferencedObjectError(CliError):
    def __init__(self, references: Dict[str, List[str]]) -> None:
        counts = " and ".join(f"{len(refs)} {name}" for name, refs in references.items())

        super().__init__(f"Cannot perform delete because it is referenced by {counts}")


class InvalidExpiryError(CliErrorWithHint):
    def __init__(self, expiry: str) -> None:
        super().__init__(
            f"Invalid expiry input: {expiry}",
            f"Accepted values are a non-zero integer followed by s, m, d, or mo. e.g. 3d",
        )


class SymIdentityNotFound(CliError):
    def __init__(self, id: str) -> None:
        super().__init__(f"No Sym Identity found for user id {id}")


class SymAPIError(CliErrorWithHint):
    """Base exception for all API errors."""


class SymAPIUnauthorizedError(SymAPIError):
    def __init__(self, error_message: str) -> None:
        super().__init__(message="You are not authorized to perform this action.", hints=error_message)


class SymAPIRequestError(SymAPIError):
    def __init__(self, message: str, request_id: str, response_code: int) -> None:
        self.response_code = response_code
        self.request_id = request_id
        super().__init__("An API error occurred!", message)

    def format_message(self):
        """Formats the error message like a CliErrorWithHint, but appends an additional contact us message after the
        hint message.
        """
        formatted_message = super().format_message()
        contact_us_text = click.style(
            (
                f"\n\nPlease contact support and include your Request ID ({self.request_id})."
                f"\nhttps://docs.symops.com/docs/support"
            ),
            fg="white",
            bold=True,
        )
        return formatted_message + contact_us_text


class SymAPIAggregateError(SymAPIRequestError):
    def __init__(self, errors: Union[str, List[str]], request_id: str, response_code: int) -> None:
        self.errors = errors if isinstance(errors, list) else [errors]
        message = "\n\n".join([error for error in self.errors])
        super().__init__(message, request_id, response_code)


class SymAPIMissingEntityError(SymAPIRequestError):
    error_codes = [404]

    def __init__(self, response_code: int, request_id: str) -> None:
        super().__init__(f"Missing entity ({response_code}).", request_id, response_code)


class SymAPIUnknownError(SymAPIRequestError):
    """Errors returned by the Sym API that we do not know how to handle."""

    def __init__(self, response_code: int, request_id: str, message: Optional[str] = None) -> None:
        if message:
            super().__init__(f"An unexpected error occurred ({response_code}): {message}", request_id, response_code)
        else:
            super().__init__(f"An unknown error with status code {response_code}.", request_id, response_code)
