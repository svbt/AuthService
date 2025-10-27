from fastapi import APIRouter, Query, HTTPException, status, Response, Depends
from fastapi.responses import RedirectResponse
from jose import JWTError

from app.core.config import settings
from app.core.security import create_access_token, verify_token
from app.core.oauth import get_amazon_client, get_amazon_session, AUTHORIZATION_BASE_URL, TOKEN_URL, PROFILE_URL, SCOPES
from app.core.kafka import publish_login_event
from app.dependencies import (
    db, 
    create_and_store_oauth_state, 
    validate_and_clear_oauth_state, 
    TokenResponse, 
    User
)
import hashlib

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/amazon/login")
async def amazon_login(response: Response):
    """Initiates the Amazon OAuth login flow."""
    client = get_amazon_client()
    state, state_hash = create_and_store_oauth_state()

    authorization_url = client.prepare_request_uri(
        AUTHORIZATION_BASE_URL,
        redirect_uri=settings.AMAZON_REDIRECT_URI,
        scope=SCOPES,
        state=state
    )
    
    response.set_cookie(key="oauth_state", value=state_hash, httponly=True, secure=False)
    return RedirectResponse(authorization_url)

@router.get("/amazon/callback", response_model=TokenResponse)
async def amazon_callback(
    code: str = Query(None),
    state: str = Query(None),
    error: str = Query(None),
    response: Response = None
):
    """Handles the Amazon OAuth callback and authenticates the user."""
    print("amazon_callback")
    if error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Amazon login failed with error: {error}")


    if not code or not state:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing code or state parameter."
        )

    state_hash = hashlib.sha256(state.encode()).hexdigest()
    if not state_hash or not validate_and_clear_oauth_state(state, state_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid state parameter (CSRF check failed).")
    
    response.set_cookie(key="oauth_state", value="", expires=0)
    amazon_session = get_amazon_session()
    
    try:
        print("amazon_callback: fetch token")
        token = amazon_session.fetch_token(
            TOKEN_URL,
            client_secret=settings.AMAZON_CLIENT_SECRET,
            code=code,
            include_client_id=True
        )
        user_profile = amazon_session.get(PROFILE_URL).json()
        user_id = user_profile.get("user_id")

        print("Token:", token)
        print("User Profile:", user_profile)
        print("User ID:", user_id)
        
        if not user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to retrieve user_id from Amazon profile.")
        
        # Database operations
        if user_id not in db:
            db[user_id] = User(id=user_id, providers=["amazon"])
            user_providers = ["amazon"]
        else:
            if "amazon" not in db[user_id].providers:
                db[user_id].providers.append("amazon")
            user_providers = db[user_id].providers

        # Publish event to Kafka
        publish_login_event(user_id, user_providers)

        # Create JWT token
        jwt_token = create_access_token({"sub": user_id, "providers": user_providers})

        print("JWT token:", jwt_token)
        
        return {"access_token": jwt_token, "token_type": "bearer"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error during Amazon OAuth flow: {str(e)}")

@router.get("/verify")
async def verify_token_endpoint(token: str):
    """Verifies a JWT token."""
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")
    return {"message": "Token is valid", "payload": payload}


