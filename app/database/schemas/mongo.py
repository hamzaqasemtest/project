from pydantic import BaseModel


class MongoSchema(BaseModel):
    @classmethod
    def from_mongo(cls, data):
        return cls(**data)

    def mongo(self, **kwargs):
        mongo_data = self.dict(by_alias=True, **kwargs)
        return mongo_data

