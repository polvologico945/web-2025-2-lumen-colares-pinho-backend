from pydantic import BaseModel


class BusInfoBase(BaseModel):
    image_url: str | None = None
    routes_text: str | None = None


class BusInfoCreate(BusInfoBase):
    pass


class BusInfoUpdate(BaseModel):
    image_url: str | None = None
    routes_text: str | None = None


class BusInfoRead(BusInfoBase):
    id: int

    class Config:
        from_attributes = True
