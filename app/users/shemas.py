from pydantic import BaseModel, ConfigDict, EmailStr


class SUserAuth(BaseModel):
    email: EmailStr
    password: str


class SUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    hashed_password: str
