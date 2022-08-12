"""Gmail tap class."""

from typing import List

from singer_sdk import Stream, Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_gmail.streams import GmailStream, MessagesStream

STREAM_TYPES = [MessagesStream]


class TapGmail(Tap):
    """Gmail tap class."""

    name = "tap-gmail"
    config_jsonschema = th.PropertiesList(
        th.Property(
            "oauth_credentials.client_id",
            th.StringType,
            description="Your google client_id",
        ),
        th.Property(
            "oauth_credentials.client_secret",
            th.StringType,
            description="Your google client_secret",
        ),
        th.Property(
            "oauth_credentials.refresh_token",
            th.StringType,
            description="Your google refresh token",
        ),
        th.Property("user_id", th.StringType, description="Your Gmail User ID"),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
