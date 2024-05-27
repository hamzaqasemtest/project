from pydantic import BaseModel, validator
from re import search


class CreateUserReq(BaseModel):
    username: str
    password: str

    @validator('username')
    def username_validator(cls, v):
        if not v or len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        if not v.isalnum():
            raise ValueError('Username must contain only alphanumeric characters')
        return v

    @validator('password')
    def password_validator(cls, v):
        if not v or len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        if not search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v


class LoginRequest(BaseModel):
    username: str
    password: str

    @validator('username')
    def username_validator(cls, v):
        if not v or len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        if not v.isalnum():
            raise ValueError('Username must contain only alphanumeric characters')
        return v

    @validator('password')
    def password_validator(cls, v):
        if not v or len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        if not search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v
