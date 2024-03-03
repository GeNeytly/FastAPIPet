from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


class BaseCrud:
    async def create_object(self, session: AsyncSession, data):
        object = self.model(**data.model_dump())
        session.add(object)
        await session.commit()
        return object
