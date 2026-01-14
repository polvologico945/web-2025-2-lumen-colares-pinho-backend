from datetime import datetime
from pydantic import BaseModel


class PostBase(BaseModel):
    conteudo: str


class PostCreate(PostBase):
    author_id: int


class PostUpdate(BaseModel):
    conteudo: str | None = None


class PostRead(PostBase):
    id: int
    data_criacao: datetime
    author_id: int

    class Config:
        orm_mode = True
