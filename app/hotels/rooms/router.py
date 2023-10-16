from fastapi import APIRouter

from app.hotels.dao import HotelsDAO
from app.hotels.shemas import SHotel

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get("/{location}")
async def get_hotels_by_location_and_time(
    location: int, date_from: int, date_to: int
) -> list[SHotel]:
    return await HotelsDAO.find_all()
