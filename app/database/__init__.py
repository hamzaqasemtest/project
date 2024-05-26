from app.database.db_manager import DatabaseManager

db_manager = DatabaseManager()


async def get_database():
    db = await db_manager.get_db()
    try:
        yield db
    finally:
        pass
