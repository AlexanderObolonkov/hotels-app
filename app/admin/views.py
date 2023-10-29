from typing import cast

from sqladmin import ModelView

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users


class UsersAdmin(ModelView, model=Users):
    column_list = [cast(str, Users.id), cast(str, Users.email)]
    column_details_exclude_list = [cast(str, Users.hashed_password)]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class HotelsAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.columns] + [
        Hotels.room,
    ]
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"


class RoomsAdmin(ModelView, model=Rooms):
    column_list = [c.name for c in Rooms.__table__.columns] + [
        Rooms.hotel,
        Rooms.booking,
    ]
    name = "Номер"
    name_plural = "Номера"
    icon = "fa-solid fa-bed"


class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.columns] + [
        Bookings.user,
        Bookings.room,
    ]
    name = "Бронь"
    name_plural = "Брони"
    icon = "fa-solid fa-book"
