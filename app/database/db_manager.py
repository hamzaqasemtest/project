from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from config import MONGO_DB_NAME,  MONGO_URL,  MONGO_USER,  MONGO_PASSWORD,  MAX_CONNECTIONS_COUNT,  MIN_CONNECTIONS_COUNT


class DatabaseManager:
    def __init__(self):
        self.db_client = None

    async def connect_and_init_db(self):
        if self.db_client is None:
            self.db_client = AsyncIOMotorClient(
                MONGO_URL,
                username=MONGO_USER,
                password=MONGO_PASSWORD,
                maxPoolSize=MAX_CONNECTIONS_COUNT,
                minPoolSize=MIN_CONNECTIONS_COUNT,
                uuidRepresentation="standard",
            )

    async def get_db(self) -> AsyncIOMotorDatabase:
        if self.db_client is None:
            await self.connect_and_init_db()
        return self.db_client[MONGO_DB_NAME]

    async def close_db_connect(self):
        if self.db_client is not None:
            self.db_client.close()
            self.db_client = None