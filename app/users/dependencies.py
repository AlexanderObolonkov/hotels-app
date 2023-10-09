from fastapi import HTTPException, Request, status


def get_token(request: Request) -> str:
    token = request.cookies.get("bookings_access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token


def get_current_user():
    ...
