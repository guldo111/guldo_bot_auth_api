# app/models/pydantic_models.py

from pydantic import BaseModel

class StoreTelegramUserRequest(BaseModel):
    """
    Pydantic model representing a request to store a Telegram user.
    
    Attributes:
        telegram_user_id (int): The Telegram user ID.
        username (str): The Telegram username.
        user_id (int): User's internal ID.
        chat_id (int): The chat ID in Telegram.
        api_key (str): API key for authentication.
        telegram_bot_token (str): The Telegram bot token.
        bot_id (Optional[int]): Optional bot ID.
    """
    telegram_user_id: int
    username: str
    user_id: int
    chat_id: int
    api_key: str
    telegram_bot_token: str
    bot_id: int = None  

class APIKeyRequest(BaseModel):
    """
    Pydantic model representing an API key request.
    
    Attributes:
        api_key (str): The API key.
    """
    api_key: str