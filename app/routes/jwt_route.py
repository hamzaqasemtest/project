from fastapi import APIRouter, Depends
from typing import Annotated
from app.common.utils import oauth2_bearer, get_current_user

router = APIRouter()


@router.post("/testjwt", response_description="Create a new user")
async def test_jwt(token: Annotated[str, Depends(oauth2_bearer)]):
    username = await get_current_user(token)
    return username


