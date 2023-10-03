from dataclasses import dataclass
from datetime import date
from typing import Optional

from fastapi import Depends, FastAPI, Query
from pydantic import BaseModel

from app.bookings.router import router as router_bookings

app = FastAPI()

app.include_router(router_bookings)


@dataclass
class HotelsSearchArgs:
    location: str
    date_from: date
    date_to: date
    has_spa: Optional[bool] = None
    stars: Optional[int] = Query(None, ge=1, le=5)


class SHotel(BaseModel):
    address: str
    name: str
    stars: int


@app.get("/hotels/")
def get_hotels(search_args: HotelsSearchArgs = Depends()):
    return search_args


class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


@app.post("/bookings")
def add_booking(booking: SBooking):
    pass
