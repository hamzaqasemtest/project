from motor.motor_asyncio import AsyncIOMotorClient
from app.database.schemas.user import User
from typing import Optional
from config import MONGO_DB_NAME


async def create_user(db_connection: AsyncIOMotorClient, username: str, password: str) -> User:
    new_user = User(username=username, password=password)
    await db_connection[MONGO_DB_NAME][User.__name__].insert_one(new_user.mongo())
    return new_user

async def get_user(db_connection: AsyncIOMotorClient, user_id: str) -> Optional[User]:
    document = await db_connection[MONGO_DB_NAME][User.__name__].find_one({"_id": user_id})
    return User.from_mongo(document) if document else None

async def get_user_by_username(db_connection: AsyncIOMotorClient, username: str) -> Optional[User]:
    document = await db_connection[MONGO_DB_NAME][User.__name__].find_one({"username": username})
    if document:
        return User.from_mongo(document)
    else:
        return None
