from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud.matricula_curso import (
    create_matricula,
    get_matricula,
    list_matriculas,
    update_matricula,
    delete_matricula,
)
from app.schemas.matricula_curso import (
    MatriculaCursoCreate,
    MatriculaCursoRead,
    MatriculaCursoUpdate,
)

router = APIRouter()


@router.post("/", response_model=MatriculaCursoRead)
def create_matricula_endpoint(
    mat_in: MatriculaCursoCreate, db: Session = Depends(get_db)
):
    return create_matricula(db=db, mat_in=mat_in)


@router.get("/", response_model=List[MatriculaCursoRead])
def list_matriculas_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return list_matriculas(db=db, skip=skip, limit=limit)


@router.get("/{matricula_id}", response_model=MatriculaCursoRead)
def get_matricula_endpoint(
    matricula_id: int,
    db: Session = Depends(get_db),
):
    mat = get_matricula(db=db, matricula_id=matricula_id)
    if not mat:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")
    return mat


@router.put("/{matricula_id}", response_model=MatriculaCursoRead)
def update_matricula_endpoint(
    matricula_id: int,
    mat_in: MatriculaCursoUpdate,
    db: Session = Depends(get_db),
):
    mat = update_matricula(db=db, matricula_id=matricula_id, mat_in=mat_in)
    if not mat:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")
    return mat


@router.delete("/{matricula_id}", status_code=204)
def delete_matricula_endpoint(
    matricula_id: int,
    db: Session = Depends(get_db),
):
    delete_matricula(db=db, matricula_id=matricula_id)
