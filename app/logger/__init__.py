import logging
import asyncio
from bson import ObjectId
from app.database.dependencies import db_manager


class AsyncMongoDBHandler(logging.Handler):
    def __init__(self, collection_name):
        super().__init__()
        self.collection_name = collection_name

    async def async_emit(self, record):
        log_entry = self.format(record)
        log_document = {
            "_id": ObjectId(),
            "timestamp": record.created,
            "level": record.levelname,
            "message": log_entry,
        }
        db = await db_manager.get_db()
        await db[self.collection_name].insert_one(log_document)

    def emit(self, record):
        asyncio.create_task(self.async_emit(record))
