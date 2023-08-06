import os
from functools import wraps

import click
from sentry_sdk import Scope
from sentry_sdk.api import configure_scope
from sentry_sdk.hub import init as sentry_init

from sym.flow.cli.helpers.config import Config
from sym.flow.cli.helpers.utils import filter_dict
from sym.flow.cli.helpers.version import is_local


def getuser():
    """Get the username from the environment or password database.

    First try various environment variables, then the password
    database.  This works on Windows as long as USERNAME is set.

    """

    for name in ("LOGNAME", "USER", "LNAME", "USERNAME"):
        user = os.environ.get(name)
        if user:
            return user

    # If this fails, the exception will "explain" why
    import pwd

    return pwd.getpwuid(os.getuid())[0]


def set_scope_context_os(scope: Scope) -> None:
    """Save the user's operating system details in the Sentry context."""

    u = os.uname()
    uname_str = f"{u.sysname} {u.nodename} {u.release} {u.version} {u.machine}"
    scope.set_context(
        "os",
        {
            "name": u.sysname,
            "version": u.release,
            "build": u.version,
            "kernel_version": uname_str,
        },
    )


def setup_sentry(**kwargs):
    """Returns a decorator that will configure Sentry before the command is invoked.
    This decorator should be set on the base `symflow` command.

    - Sets the environment to `pypi`
    - Initializes the Sentry SDK
    - Sets Sentry tags identifying the user and their org
    - Sets the OS details in the Sentry context
    """
    environment = "pypi"
    sample_rate = 0.0 if is_local() else 1.0  # Don't send anything to Sentry for local testing
    sentry_init(environment=environment, sample_rate=sample_rate, **kwargs)

    def decorator(fn):
        @click.pass_context
        @wraps(fn)
        def wrapped(context: click.Context, *args, **kwargs):
            with configure_scope() as scope:
                # Set custom tags for Sentry alerts
                if org_slug := Config.get_org_slug():
                    scope.set_tag("org", org_slug)

                user = filter_dict({"username": getuser(), "email": Config.get_email()})
                scope.set_user(user)

                set_scope_context_os(scope)

                # Invoke the command
                return context.invoke(fn, *args, **kwargs)

        return wrapped

    return decorator
