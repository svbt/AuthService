from fastapi import FastAPI
from app.api.v1.endpoints import auth

# Create the FastAPI application instance
app = FastAPI(title="AuthService API")

# Include the authentication router
app.include_router(auth.router, prefix="/api/v1")

# The server will be started by the 'uvicorn' command in the Dockerfile
# and will automatically detect and run this `app` instance.

