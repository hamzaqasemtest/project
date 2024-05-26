import uuid
from langchain_openai import AzureChatOpenAI
from config import AZURE_CHATBOT_API_KEY, AZURE_CHATBOT_ENDPOINT, AZURE_CHATBOT_OPENAI_VERSION
from datetime import timedelta, datetime
from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status
from config import SECRET_KEY, ALGORITHM


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def create_access_token(username: str, expires_delta: timedelta):
    encode = {"sub": username}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )
        return {"username": username}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user."
        )

def get_llm():
    llm_instance = AzureChatOpenAI(
        api_key=AZURE_CHATBOT_API_KEY,
        azure_endpoint=AZURE_CHATBOT_ENDPOINT,
        openai_api_version=AZURE_CHATBOT_OPENAI_VERSION,
    )

    return llm_instance


def generate_uuid_str():
    return str(uuid.uuid4())


