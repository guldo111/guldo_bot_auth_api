from typing import Dict, Any
from fastapi import HTTPException
from app.services.general_db import GeneralDB
from app.utils.database import get_database_connection
from app.utils.security import encrypt_data, decrypt_data
from telegram import Bot, Update


class TelegramDB:

    @staticmethod
    def check_entitlements(api_key: str, conn) -> Dict[str, Any]:
        """
        Verify the API key and check if the user is entitled to Telegram features.
        """
        # Use the GeneralDB method to validate the API key and check for telegram entitlement
        db_response = GeneralDB.validate_api_key(api_key, conn)
        entitlements = db_response.get("entitlements", {})

        if "telegram" not in entitlements.get("plugins", []):
            raise HTTPException(status_code=403, detail="Telegram plugin not enabled for this API key.")
        
        return db_response
    
    @staticmethod
    def get_existing_telegram_user(user_id: int, conn) -> str:
        """
        Check if the user already exists in the telegram_users table and return the chat_id.
        """
        query = "SELECT chat_id FROM telegram_users WHERE user_id = %s"
        
        with conn.cursor() as cursor:
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            if result:
                return decrypt_data(result[0])  # Decrypt the stored chat_id before returning it
            return None  # No existing telegram user found

    @staticmethod
    def search_and_store_telegram_user(user_id: int, telegram_bot_token: str, conn) -> Dict[str, Any]:
        """
        Polls the bot for new messages, retrieves user info, and stores it in the telegram_users table.
        """
        bot = Bot(token=telegram_bot_token)
        updates = bot.get_updates(timeout=10)

        if not updates:
            raise HTTPException(status_code=404, detail="No new messages received from the bot.")

        # Process updates and store the first valid user's data
        for update in updates:
            chat_id = update.message.chat.id
            telegram_user_id = update.message.from_user.id
            username = update.message.from_user.username
            
            encrypted_chat_id = encrypt_data(str(chat_id))
            encrypted_telegram_user_id = encrypt_data(str(telegram_user_id))
            encrypted_username = encrypt_data(username) if username else None

            query = """
                INSERT INTO telegram_users (telegram_user_id, username, user_id, chat_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (telegram_user_id) DO UPDATE 
                SET chat_id = EXCLUDED.chat_id, username = EXCLUDED.username
            """

            with conn.cursor() as cursor:
                cursor.execute(query, (encrypted_telegram_user_id, encrypted_username, user_id, encrypted_chat_id))
                conn.commit()

            return {
                "message": "User stored successfully",
                "chat_id": chat_id,
                "telegram_user_id": telegram_user_id
            }

    @staticmethod
    def get_or_create_telegram_user(api_key: str, conn) -> Dict[str, Any]:
        """
        Main function to get or create a Telegram user using the bot token.
        """
        # Step 1: Validate the API key and check for entitlements
        db_response = TelegramDB.check_entitlements(api_key, conn)
        user_id = db_response["user_id"]

        # Step 2: Check if the user already has a telegram chat_id assigned
        existing_chat_id = TelegramDB.get_existing_telegram_user(user_id, conn)

        # Step 3: Fetch the bot token from the telegram_bots table
        query = "SELECT telegram_bot_token FROM telegram_bots LIMIT 1"
        
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="No bot token found in telegram_bots table.")

            telegram_bot_token = decrypt_data(result[0])

        # If chat_id exists, return it with the bot token
        if existing_chat_id:
            return {
                "message": "Chat ID found",
                "chat_id": existing_chat_id,
                "telegram_bot_token": telegram_bot_token
            }

        # Step 4: If no chat_id, use bot token to poll messages and store user info
        result = TelegramDB.search_and_store_telegram_user(user_id, telegram_bot_token, conn)
        return {
            "message": result["message"],
            "chat_id": result["chat_id"],
            "telegram_bot_token": telegram_bot_token
        }

    @staticmethod
    def store_telegram_user(telegram_user_id: int, username: str, api_key: str, telegram_bot_token: str) -> Dict[str, Any]:
        """
        Store the Telegram user's data in the database, encrypting sensitive information.
        """
        encrypted_telegram_user_id = encrypt_data(str(telegram_user_id))
        encrypted_username = encrypt_data(username)
        encrypted_bot_token = encrypt_data(telegram_bot_token)

        query = """
            INSERT INTO telegram_users (telegram_user_id, username, api_key, telegram_bot_token)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (telegram_user_id) DO UPDATE 
            SET username = EXCLUDED.username, telegram_bot_token = EXCLUDED.telegram_bot_token
        """

        with next(get_database_connection()) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (encrypted_telegram_user_id, encrypted_username, api_key, encrypted_bot_token))
                conn.commit()

        return {"message": "Telegram user stored successfully."}