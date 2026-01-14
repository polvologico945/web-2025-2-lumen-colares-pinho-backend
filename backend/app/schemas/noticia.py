from pydantic import BaseModel


class NoticiaBase(BaseModel):
    title: str
    content: str
    active: bool = True
    type: str
    created_by: int


class NoticiaCreate(NoticiaBase):
    pass

class NoticiaUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    active: bool | None = None
    type: str | None = None

class NoticiaRead(NoticiaBase):
    id: int

    class Config:
        orm_mode = True
