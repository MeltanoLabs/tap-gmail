"""Gmail Authentication."""


from singer_sdk.authenticators import OAuthAuthenticator, SingletonMeta


# The SingletonMeta metaclass makes your streams reuse the same authenticator instance.
# If this behaviour interferes with your use-case, you can remove the metaclass.
class GmailAuthenticator(OAuthAuthenticator, metaclass=SingletonMeta):
    """Authenticator class for Gmail."""

    @property
    def oauth_request_body(self) -> dict:
        """Define the OAuth request body for the Gmail API."""
        oauth_credentials = self.config.get("oauth_credentials", {})
        return {
            "grant_type": "refresh_token",
            "client_id": oauth_credentials.get("client_id"),
            "client_secret": oauth_credentials.get("client_secret"),
            "refresh_token": oauth_credentials.get("refresh_token"),
        }

    @classmethod
    def create_for_stream(cls, stream) -> "GmailAuthenticator":
        return cls(
            stream=stream,
            auth_endpoint="https://oauth2.googleapis.com/token",
            oauth_scopes="https://www.googleapis.com/auth/gmail.readonly",
        )
