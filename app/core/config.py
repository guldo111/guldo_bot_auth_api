from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    """
    Holds configuration settings for the application.

    Attributes:
        database_url (str): The URL for the database connection.
        encryption_key (str): The encryption key for securing data.
    """
    # Check if Railway secrets are available, otherwise fall back to .env
    database_url: str = os.getenv("DATABASE_URL", None) or "postgresql://user:password@localhost/dbname"
    encryption_key: str = os.getenv("ENCRYPTION_KEY", None) or "default_key"

    class Config:
        env_file = ".env"  # This will be used if no environment variables are found.

# Create an instance of the Settings class that can be used throughout the app
settings = Settings()