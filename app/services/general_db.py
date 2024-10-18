from fastapi import HTTPException
from psycopg2 import connect, OperationalError
from app.utils.database import get_database_connection
from typing import Dict, Any

class GeneralDB:
    """
    Handles database operations related to general tasks, such as API key validation.
    """

    @staticmethod
    def validate_api_key(api_key: str, conn) -> Dict[str, Any]:
        """
        Validates the provided API key.

        Args:
            api_key (str): The API key to validate.
            conn (Any): Database connection object.

        Returns:
            Dict[str, Any]: The validation result including user_id and entitlements.

        Raises:
            HTTPException: If the API key is invalid or a database error occurs.
        """
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT user_id, entitlements FROM premium_api_keys WHERE api_key = %s AND is_active = TRUE", 
                    (api_key,)
                )
                result = cursor.fetchone()

                if not result:
                    raise HTTPException(status_code=401, detail="Invalid API key")

                user_id, entitlements = result
                return {"user_id": user_id, "entitlements": entitlements}

        except OperationalError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {e}")