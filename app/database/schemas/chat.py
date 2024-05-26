from pydantic import Field
from app.database.schemas.mongo import MongoSchema
from app.common.utils import generate_uuid_str


class Chat(MongoSchema):
    id: str = Field(default_factory=generate_uuid_str, alias='_id')
    username: str
    title: str
    session: dict
