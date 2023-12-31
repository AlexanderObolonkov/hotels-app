from datetime import date

from sqlalchemy import and_, func, insert, or_, select
from sqlalchemy.exc import SQLAlchemyError

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms
from app.logger import logger  # type: ignore


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(  # type: ignore[override]
        cls, user_id: int, room_id: int, date_from: date, date_to: date
    ):
        """
        WITH booked_rooms AS (SELECT *
                      FROM bookings
                      WHERE room_id = 1
                          AND (date_from >= '2023-05-15' AND date_from <= '2023-06-20')
                         OR (date_from <= '2023-05-15' AND date_to > '2023-05-15'))
        SELECT rooms.quantity - count(booked_rooms.room_id)
        FROM rooms
                 LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id;
        """
        try:
            async with async_session_maker() as session:
                booked_rooms = (
                    select(Bookings)
                    .where(
                        and_(
                            Bookings.room_id == room_id,
                            or_(
                                and_(
                                    Bookings.date_from >= date_from,
                                    Bookings.date_from <= date_to,
                                ),
                                and_(
                                    Bookings.date_from <= date_from,
                                    Bookings.date_to > date_from,
                                ),
                            ),
                        )
                    )
                    .cte("booked_rooms")
                )

                get_rooms_left = (
                    select(
                        (Rooms.quantity - func.count(booked_rooms.c.room_id)).label(
                            "rooms_left"
                        )
                    )
                    .select_from(Rooms)
                    .join(
                        booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
                    )
                    .where(Rooms.id == room_id)
                    .group_by(Rooms.quantity, booked_rooms.c.room_id)
                )
                # print(
                #     rooms_left.compile(
                #         engine,
                #         compile_kwargs={"literal_binds": True},
                #     )
                # )
                query = await session.execute(get_rooms_left)

                rooms_left: int = query.scalar_one()

                if rooms_left > 0:
                    get_price = select(Rooms.price).filter_by(id=room_id)
                    query = await session.execute(get_price)
                    price: int = query.scalar_one()
                    add_booking = (
                        insert(Bookings)
                        .values(
                            room_id=room_id,
                            user_id=user_id,
                            date_from=date_from,
                            date_to=date_to,
                            price=price,
                        )
                        .returning(Bookings)
                    )

                    new_booking = await session.execute(add_booking)
                    await session.commit()
                    return new_booking.scalar_one()
                else:
                    return None
        except (SQLAlchemyError, Exception) as error:
            if isinstance(error, SQLAlchemyError):
                message = "Database exception"
            else:
                message = "Unknown exception"
            extra = {
                "user_id": user_id,
                "room_id": room_id,
                "date_from": date_from,
                "date_to": date_to,
            }
            logger.error(f"{message}: Cannot add booking", extra=extra, exc_info=True)
