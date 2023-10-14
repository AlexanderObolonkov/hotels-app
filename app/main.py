from dataclasses import dataclass
from datetime import date
from typing import Optional

from fastapi import Depends, FastAPI, Query

from app.bookings.router import router as router_bookings
from app.users.router import router as router_users

app = FastAPI()

app.include_router(router_users)
app.include_router(router_bookings)


@dataclass
class HotelsSearchArgs:
    location: str
    date_from: date
    date_to: date
    has_spa: Optional[bool] = None
    stars: Optional[int] = Query(None, ge=1, le=5)


@app.get("/hotels/")
def get_hotels(search_args: HotelsSearchArgs = Depends()):
    return search_args
