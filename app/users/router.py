from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.users.auth import _get_password_hash, authenticate_user, create_access_token
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.shemas import SUser, SUserAuth

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"],
)


@router.post("/register")
async def register_user(user_data: SUserAuth) -> None:
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    hashed_password = _get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth) -> dict[str, str]:
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("bookings_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response) -> dict[str, str]:
    response.delete_cookie("bookings_access_token")
    return {"OK": "user logout"}


@router.get("/me")
async def get_info_about_current_user(
    current_user: Users = Depends(get_current_user),
) -> SUser:
    return SUser.model_validate(current_user)
