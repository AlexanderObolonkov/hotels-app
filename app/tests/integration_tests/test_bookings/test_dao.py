from datetime import date

from app.bookings.dao import BookingDAO


async def test_and_get_booking():
    new_booking = await BookingDAO.add(
        user_id=2,
        room_id=2,
        date_from=date(2023, 7, 10),
        date_to=date(2023, 7, 24),
    )

    assert new_booking.user_id == 2
    assert new_booking.room_id == 2

    new_booking = await BookingDAO.find_one_or_none(id=new_booking.id)

    assert new_booking is not None
