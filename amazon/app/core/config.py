import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    AMAZON_CLIENT_ID: str = os.getenv("AMAZON_CLIENT_ID")
    AMAZON_CLIENT_SECRET: str = os.getenv("AMAZON_CLIENT_SECRET")
    AMAZON_REDIRECT_URI: str = os.getenv("AMAZON_REDIRECT_URI")
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    KAFKA_USER_TOPIC: str = os.getenv("KAFKA_USER_TOPIC", "user.login")
    ENV: str = os.getenv("ENV", "local")

settings = Settings()
