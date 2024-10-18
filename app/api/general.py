from fastapi import APIRouter
from models.pydantic_models import APIKeyRequest
from services.general_db import GeneralDB

router = APIRouter()

@router.post("/validate-api-key")
def validate_api_key(request: APIKeyRequest):
    """
    Validates the provided API key.

    Args:
        request (APIKeyRequest): API key payload.

    Returns:
        Dict[str, Any]: The validation result including user_id and entitlements.
    """
    return GeneralDB.validate_api_key(request.api_key)