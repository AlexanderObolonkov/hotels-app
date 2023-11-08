import asyncio
import json
from datetime import datetime
from typing import Any, AsyncGenerator, Generator

import pytest
from httpx import AsyncClient
from sqlalchemy import insert

from app.bookings.models import Bookings
from app.config import settings
from app.database import Base, async_session_maker, engine
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.main import app as fastapi_app
from app.users.models import Users


@pytest.fixture(scope="session", autouse=True)
async def prepare_database() -> None:
    if settings.MODE != "TEST":
        raise Exception("Not 'TEST' mode for testing")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str) -> list[dict]:
        with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    hotels = open_mock_json("hotels")
    rooms = open_mock_json("rooms")
    users = open_mock_json("users")
    bookings = open_mock_json("bookings")

    for booking in bookings:
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")

    async with async_session_maker() as session:
        for model, values in [
            (Hotels, hotels),
            (Rooms, rooms),
            (Users, users),
            (Bookings, bookings),
        ]:
            query = insert(model).values(values)
            await session.execute(query)

        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request) -> Generator[asyncio.AbstractEventLoop, Any, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def get_async_client() -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac
