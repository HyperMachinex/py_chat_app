from celery_worker import celery_app
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
import asyncio

mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(mongo_uri)
db = client["chat_app"]
messages_collection = db["messages"]

@celery_app.task
def delete_message_task(message_id: str):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_delete_message(message_id))

async def _delete_message(message_id: str):
    await messages_collection.update_one(
        {"_id": ObjectId(message_id)},
        {"$set": {"message": "Deleted.", "deleted": True}}
    )
