from fastapi import APIRouter, Depends, HTTPException
from app.models.pydantic_models import APIKeyRequest
from app.services.general_db import GeneralDB
from app.utils.database import get_database_connection
from typing import Any, Dict

router = APIRouter()

@router.post("/validate-api-key")
def validate_api_key(request: APIKeyRequest, conn=Depends(get_database_connection)):
    """
    Validates the provided API key.

    Args:
        request (APIKeyRequest): API key payload.
        conn (Any): Database connection dependency.

    Returns:
        Dict[str, Any]: The validation result including user_id and entitlements.
    """
    try:
        return GeneralDB.validate_api_key(request.api_key, conn)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")