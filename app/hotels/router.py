from datetime import date

from fastapi import APIRouter

from app.exceptions import CannotBookHotelForLongPeriod, DateFromCannotBeAfterDateTo
from app.hotels.dao import HotelsDAO
from app.hotels.shemas import SHotel

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get("/{location}")
async def get_hotels_by_location_and_time(
    location: str, date_from: date, date_to: date
) -> list[SHotel]:
    if date_from > date_to:
        raise DateFromCannotBeAfterDateTo
    if (date_to - date_from).days > 31:
        raise CannotBookHotelForLongPeriod
    hotels = await HotelsDAO.find_all(location, date_from, date_to)
    return hotels
