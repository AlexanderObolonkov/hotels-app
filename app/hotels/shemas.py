from pydantic import BaseModel, ConfigDict


class SHotel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ...
