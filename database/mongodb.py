from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv, find_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
from datetime import datetime, timezone

DB_NAME=os.getenv("DB_NAME")

class ChatHistoryManager:
    def __init__(self, collection_name, db_name=DB_NAME):
        """Initialize the MongoDB connection and select the database and collection."""
        load_dotenv(find_dotenv())
        mongo_uri = os.getenv("MONGO_DB_CLUSTER_URL")
        
        if not mongo_uri:
            raise ValueError("MongoDB connection string is missing in environment variables.")
        
        self.client = MongoClient(mongo_uri, server_api=ServerApi("1"))
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def save_chat_history(self, user_id, role, message):
        """Save chat messages in MongoDB."""
        chat_entry = {
            "user_id": user_id,
            "role": role,  # "user" or "model"
            "message": message,
            "timestamp": datetime.now(timezone.utc)
        }
        self.collection.insert_one(chat_entry)

    def get_recent_chat_history(self, user_id, limit=10):
        """Retrieve the most recent chat messages for a user."""
        messages = (
            self.collection.find({"user_id": user_id})
            .sort("timestamp", -1)
            .limit(limit)
        )
        return [{"role": msg["role"], "parts": [msg["message"]]} for msg in messages]

# Example usage:
# chat_manager = ChatHistoryManager()
# chat_manager.save_chat_history("user123", "user", "Hello, how are you?")
# history = chat_manager.get_recent_chat_history("user123")
# print(history)
