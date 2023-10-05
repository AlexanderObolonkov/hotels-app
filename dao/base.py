from typing import Optional

from sqlalchemy import RowMapping, select

from app.database import Base, async_session_maker


class BaseDAO:
    model: Optional[type[Base]] = None

    @classmethod
    async def find_one_or_none(cls, **filter_by) -> RowMapping | None:
        async with async_session_maker() as session:
            query = select().filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls, **filter_by) -> RowMapping | None:
        async with async_session_maker() as session:
            query = select().filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()
