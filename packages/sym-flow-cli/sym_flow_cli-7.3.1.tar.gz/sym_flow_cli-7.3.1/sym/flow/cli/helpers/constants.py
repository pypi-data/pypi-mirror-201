from enum import Enum

SentryDSN = "https://6a8722276347467b801e5aa152a48ed1@o373009.ingest.sentry.io/5462801"

DEFAULT_API_URL = "https://api.symops.com/api/v1"
DEFAULT_AUTH_URL = "https://auth.symops.com"

CLI_PACKAGE_NAME = "sym-flow-cli"

SYM_DOCUMENTATION_URL = "https://docs.symops.com/"
SYM_SUPPORT_EMAIL = "support@symops.com"


class SegmentTrackStatus(str, Enum):
    """Accepted statuses for the segment_track Sym API call."""

    INVOKED = "invoked"
    SUCCESS = "success"
    ERROR = "error"
