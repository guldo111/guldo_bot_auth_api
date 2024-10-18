from fastapi import APIRouter
from models.pydantic_models import APIKeyRequest
from services.telegram_db import TelegramDB

router = APIRouter()

@router.post("/get-or-create-telegram-user")
def get_or_create_telegram_user(request: APIKeyRequest):
    """
    Gets or creates a Telegram user.

    Args:
        request (APIKeyRequest): API key payload.

    Returns:
        Dict[str, Any]: Telegram user details.
    """
    return TelegramDB.get_or_create_telegram_user(request.api_key)