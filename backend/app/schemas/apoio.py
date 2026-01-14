from datetime import datetime
from pydantic import BaseModel


class ApoioBase(BaseModel):
    user_id: int
    post_id: int


class ApoioCreate(ApoioBase):
    pass


class ApoioRead(ApoioBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
