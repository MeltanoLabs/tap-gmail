"""Stream type classes for tap-gmail."""

from pathlib import Path

from tap_gmail.client import GmailStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class MessagesStream(GmailStream):
    """Define custom stream."""

    name = "messages"
    primary_keys = ["id"]
    replication_key = None
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    schema_filepath = SCHEMAS_DIR / "messages.json"

    @property
    def path(self):
        """Set the path for the stream."""
        return "/gmail/v1/users/" + self.config["user_id"] + "/messages"
