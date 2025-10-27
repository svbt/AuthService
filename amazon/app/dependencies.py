from pydantic import BaseModel
from fastapi import Request
import secrets
import hashlib

# --- Dummy Database (replace with actual database in production) ---
db = {}
state_store = {}

class User(BaseModel):
    id: str
    providers: list[str]

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

def create_and_store_oauth_state() -> tuple[str, str]:
    """Generates a secure state parameter and stores its hash."""
    state = secrets.token_urlsafe(32)
    state_hash = hashlib.sha256(state.encode()).hexdigest()
    state_store[state_hash] = state
    return state, state_hash

def validate_and_clear_oauth_state(state: str, state_hash: str) -> bool:
    """Validates the state parameter and clears it from the store."""
    if state_hash not in state_store or state_store[state_hash] != state:
        return False
    del state_store[state_hash]
    return True

