from oauthlib.oauth2 import WebApplicationClient
from requests_oauthlib import OAuth2Session

from app.core.config import settings

# --- OAuth URLs and Scopes ---
AUTHORIZATION_BASE_URL = "https://www.amazon.com/ap/oa"
TOKEN_URL = "https://api.amazon.com/auth/o2/token"
PROFILE_URL = "https://api.amazon.com/user/profile"
SCOPES = "profile:user_id"

def get_amazon_client() -> WebApplicationClient:
    """Initializes the OAuth2 client for Amazon."""
    return WebApplicationClient(settings.AMAZON_CLIENT_ID)

def get_amazon_session(redirect_uri: str = settings.AMAZON_REDIRECT_URI) -> OAuth2Session:
    """Initializes the OAuth2 session for Amazon."""
    return OAuth2Session(settings.AMAZON_CLIENT_ID, redirect_uri=redirect_uri)

