from pydantic import BaseModel


class InterestBase(BaseModel):
    nome: str


class InterestCreate(InterestBase):
    pass


class InterestUpdate(BaseModel):
    nome: str | None = None


class InterestRead(InterestBase):
    id: int

    class Config:
        from_attributes = True
