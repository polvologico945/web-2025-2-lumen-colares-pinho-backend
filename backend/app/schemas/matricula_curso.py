from pydantic import BaseModel


class MatriculaCursoBase(BaseModel):
    user_id: int
    subject_name: str
    period: str


class MatriculaCursoCreate(MatriculaCursoBase):
    pass


class MatriculaCursoUpdate(BaseModel):
    subject_name: str | None = None
    period: str | None = None


class MatriculaCursoRead(MatriculaCursoBase):
    id: int

    class Config:
        from_attributes = True
