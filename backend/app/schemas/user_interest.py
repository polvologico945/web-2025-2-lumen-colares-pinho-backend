from pydantic import BaseModel


class UserInterestBase(BaseModel):
    user_id: int
    interest_id: int


class UserInterestCreate(UserInterestBase):
    pass


class UserInterestRead(UserInterestBase):
    id: int

    class Config:
        orm_mode = True
