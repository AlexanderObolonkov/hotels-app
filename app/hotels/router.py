from datetime import date

from fastapi import APIRouter

from app.exceptions import CannotBookHotelForLongPeriod, DateFromCannotBeAfterDateTo
from app.hotels.dao import HotelsDAO
from app.hotels.rooms.router import router as router_room
from app.hotels.schemas import SHotel

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)
router.include_router(router_room)


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
