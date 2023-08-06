from typing import Any

from click import Command, Context

from sym.flow.cli.errors import SymAPIRequestError
from sym.flow.cli.helpers.constants import SegmentTrackStatus
from sym.flow.cli.helpers.global_options import GlobalOptions


class TrackedCommand(Command):
    """A custom Click Command that makes API calls to Queuer to track the command's invocation and success/fail statuses
    in Segment. Pass this in as the `cls` argument to the `@click.command` decorator for any symflow commands that
    should be tracked.

    For example:
    @click.command(cls=TrackedCommand, short_help="foo")
    def foo():
       ...
    """

    def invoke(self, ctx: Context) -> Any:
        # Pull the Global Options out of Click's magical Context.
        # This should always exist because we decorate all of our commands with
        # `@click.make_pass_decorator(GlobalOptions, ensure=True)`
        options: GlobalOptions
        if (options := ctx.find_object(GlobalOptions)) and options.sym_api.rest.access_token:

            # ctx.command_path returns the full command path starting from `symflow` (e.g. "symflow bots list").
            # We only want the subcommands, so strip the initial "symflow ".
            subcommand = ctx.command_path.replace("symflow ", "")

            options.sym_api.segment_track(subcommand, status=SegmentTrackStatus.INVOKED)
            try:
                result = super().invoke(ctx)
            except Exception as e:
                if isinstance(e, SymAPIRequestError):
                    # e.message for SymAPIRequestErrors are always "An API error occurred!", with the actual error
                    # is reflected in the hint message.
                    error_message = ", ".join(e.hints)
                else:
                    error_message = getattr(e, "message", str(e))
                options.sym_api.segment_track(subcommand, status=SegmentTrackStatus.ERROR, error=error_message)
                raise e

            options.sym_api.segment_track(subcommand, status=SegmentTrackStatus.SUCCESS)
            return result

        # If we don't have  Global Options or the user isn't logged in, then we can't track the command.
        # Just invoke the command normally.
        return super().invoke(ctx)
