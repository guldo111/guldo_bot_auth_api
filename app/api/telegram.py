from fastapi import APIRouter, Depends, HTTPException
from app.models.pydantic_models import APIKeyRequest
from app.services.general_db import GeneralDB
from app.services.telegram_db import TelegramDB
from app.utils.database import get_database_connection
from typing import Any, Dict

router = APIRouter()

@router.post("/get-or-create-telegram-user")
def get_or_create_telegram_user(request: APIKeyRequest, conn=Depends(get_database_connection)):
    """
    Gets or creates a Telegram user.
    
    Args:
        request (APIKeyRequest): API key payload.
        conn (Any): Database connection dependency.

    Returns:
        Dict[str, Any]: Telegram user details.
    """
    try:
        # Validate API key first
        telegram_user_details = TelegramDB.get_or_create_telegram_user(request.api_key, conn)
        return telegram_user_details
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")