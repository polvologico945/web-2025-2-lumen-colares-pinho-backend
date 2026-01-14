from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr
    idade: int | None = None
    cidade: str | None = None
    bio: str | None = None
    empresa: str | None = None
    avatar_url: str | None = None
    papel: str = "user"
    curso: str | None = None
    semestre: str | None = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: str | None = None
    idade: int | None = None
    cidade: str | None = None
    bio: str | None = None
    empresa: str | None = None
    avatar_url: str | None = None
    papel: str | None = None
    curso: str | None = None
    semestre: str | None = None


class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True

#
class UserLogin(BaseModel):
    email: EmailStr
    password: str