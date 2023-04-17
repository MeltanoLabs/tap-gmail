"""Stream type classes for tap-gmail."""

from base64 import urlsafe_b64decode
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from bs4 import BeautifulSoup
from tap_gmail.client import GmailStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class MessageListStream(GmailStream):
    """Define custom stream."""

    name = "message_list"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "message_list.json"
    records_jsonpath = "$.messages[*]"
    next_page_token_jsonpath = "$.nextPageToken"

    @property
    def path(self):
        """Set the path for the stream."""
        return "/gmail/v1/users/" + self.config["user_id"] + "/messages"

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {"message_id": record["id"]}

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        config = self.config.get("messages", {})

        params = super().get_url_params(context, next_page_token)
        params["includeSpamTrash"] = config.get("include_spam_trash")
        params["q"] = config.get("q")
        return params


class MessagesStream(GmailStream):

    name = "messages"
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "messages.json"
    parent_stream_type = MessageListStream
    ignore_parent_replication_keys = True
    state_partitioning_keys = []

    @property
    def path(self):
        """Set the path for the stream."""
        return "/gmail/v1/users/" + self.config["user_id"] + "/messages/{message_id}"

    def get_records(self, context: dict | None):
        """Return a generator of row-type dictionary objects.

        Each row emitted should be a dictionary of property names to their values.
        """
        for record in super().get_records(context):
            yield {
                **record,
                "date": datetime.utcfromtimestamp(int(record.get("internalDate", "0"))/1000).isoformat(),
                "body": self._body_from_message_part(record.get("payload", {}))
            }

    def _body_from_message_part(self, part):
        base64_data = part.get("body", {}).get("data")
        data = urlsafe_b64decode(base64_data).decode("utf-8") if base64_data else ""

        if part.get("mimeType") == "text/plain":
            return {"text": data, "html": None}

        if part.get("mimeType") == "text/html":
            text = BeautifulSoup(data).get_text()
            return {"text": text, "html": data}

        body = {"text": None, "html": None}
        for subpart in part.get("parts", []):
            part_body = self._body_from_message_part(subpart)
            if part_body.get("html"):
                body["html"] = part_body["html"]
            if part_body.get("text"):
                body["text"] = part_body["text"]

        return body
