from beanie import Document
from time import timezone


class BaseModel(Document):
    @classmethod
    async def create(cls, **kwargs):
        return await cls(**kwargs).insert()

    @classmethod
    async def from_id(cls, id: str, **kwargs):
        if id:
            try:
                return await cls.get(id,  **kwargs)
            except:
                pass

    def get_create_at_utc_timestamp(self):
        return self.id.generation_time.timestamp() + timezone

    @classmethod
    async def get_or_create(cls, **kwargs):
        if model := await cls.find_one(kwargs):
            return model, False
        return await cls.create(**kwargs), True

    async def update_doc(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return await self.save()

    @classmethod
    async def update_or_create(cls, id: str, **kwargs):
        if model := await cls.from_id(id):
            return await model.update_doc(**kwargs)
        return await cls.create(**kwargs)
