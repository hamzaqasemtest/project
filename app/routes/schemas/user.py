from pydantic import BaseModel, Field, validator

class CreateUserReq(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str


    # @validator('username')
    # def username_validator(cls, v):
    #     if not v or len(v) < 3:
    #         raise ValueError('Username must be at least 3 characters long')
    #     return v

    # @validator('password')
    # def password_validator(cls, v):
    #     if not v or len(v) < 8:
    #         raise ValueError('Password must be at least 8 characters long')
    #     return v
