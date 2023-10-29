from typing import cast

from sqladmin import ModelView

from app.bookings.models import Bookings
from app.users.models import Users


class UsersAdmin(ModelView, model=Users):  # type: ignore
    column_list = [cast(str, Users.id), cast(str, Users.email)]
    column_details_exclude_list = [cast(str, Users.hashed_password)]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class BookingsAdmin(ModelView, model=Bookings):  # type: ignore
    column_list = [c.name for c in Bookings.__table__.columns] + [Bookings.user]
    name = "Бронь"
    name_plural = "Брони"
