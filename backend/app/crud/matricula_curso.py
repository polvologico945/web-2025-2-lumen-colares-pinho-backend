from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.matricula_curso import MatriculaCurso
from app.schemas.matricula_curso import (
    MatriculaCursoCreate,
    MatriculaCursoUpdate,
)


def get_matricula(db: Session, matricula_id: int) -> Optional[MatriculaCurso]:
    return (
        db.query(MatriculaCurso)
        .filter(MatriculaCurso.id == matricula_id)
        .first()
    )


def list_matriculas(
    db: Session, skip: int = 0, limit: int = 100
) -> List[MatriculaCurso]:
    return (
        db.query(MatriculaCurso)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_matricula(
    db: Session, mat_in: MatriculaCursoCreate
) -> MatriculaCurso:
    db_mat = MatriculaCurso(**mat_in.dict())
    db.add(db_mat)
    db.commit()
    db.refresh(db_mat)
    return db_mat


def update_matricula(
    db: Session, matricula_id: int, mat_in: MatriculaCursoUpdate
) -> Optional[MatriculaCurso]:
    db_mat = get_matricula(db, matricula_id)
    if not db_mat:
        return None

    data = mat_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(db_mat, field, value)

    db.commit()
    db.refresh(db_mat)
    return db_mat


def delete_matricula(db: Session, matricula_id: int) -> None:
    db.query(MatriculaCurso).filter(
        MatriculaCurso.id == matricula_id
    ).delete()
    db.commit()
