from app.database.schemas.mongo import MongoSchema
from pydantic import Field
from app.common.utils import generate_uuid_str


class User(MongoSchema):
    id: str = Field(default_factory=generate_uuid_str, alias='_id')
    username: str
    password: str
