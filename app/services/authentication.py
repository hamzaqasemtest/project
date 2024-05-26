import hashlib

from motor.motor_asyncio import AsyncIOMotorClient
from app.services.database import create_user, get_user_by_username
from app.database.schemas.user import User


class AuthService:

    async def register(self, db: AsyncIOMotorClient, username: str, password: str) -> User:
        """
        Register a new user with the given username and password. If a user with the
        same username already exists, an exception will be thrown.

        Args:
            username (str): The username of the new user.
            password (str): The password of the new user.
            db (AsyncIOMotorClient): The database connection to use.
        Returns:
            bool: True if the registration was successful, False otherwise.
        """
        user = await create_user(db, username, self.hash_password(password))
        return user

    async def login(self, db: AsyncIOMotorClient, username: str, password: str) -> User:
        """
        Attempt to log in with the given username and password.

        Args:
            username (str): The username to log in with.
            password (str): The password to log in with.
            db (AsyncIOMotorClient): The database connection to use.
        Returns:
            bool: True if the login was successful, False otherwise.
        """
        existing_user = await get_user_by_username(db, username)
        if existing_user and self.hash_password(password) == existing_user.password:
            return existing_user
        return None


    @staticmethod
    def hash_password(password):
        sha_signature = hashlib.sha256(password.encode()).hexdigest()
        return sha_signature
