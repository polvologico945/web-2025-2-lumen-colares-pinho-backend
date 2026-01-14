from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud.post import (
    create_post,
    get_post,
    list_posts,
    update_post,
    delete_post,
)
from app.schemas.post import PostCreate, PostRead, PostUpdate

router = APIRouter()


@router.post("/", response_model=PostRead)
def create_post_endpoint(
    post_in: PostCreate, db: Session = Depends(get_db)
):
    return create_post(db=db, post_in=post_in)


@router.get("/", response_model=List[PostRead])
def list_posts_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return list_posts(db=db, skip=skip, limit=limit)


@router.get("/{post_id}", response_model=PostRead)
def get_post_endpoint(
    post_id: int,
    db: Session = Depends(get_db),
):
    post = get_post(db=db, post_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post não encontrado")
    return post


@router.put("/{post_id}", response_model=PostRead)
def update_post_endpoint(
    post_id: int,
    post_in: PostUpdate,
    db: Session = Depends(get_db),
):
    post = update_post(db=db, post_id=post_id, post_in=post_in)
    if not post:
        raise HTTPException(status_code=404, detail="Post não encontrado")
    return post


@router.delete("/{post_id}", status_code=204)
def delete_post_endpoint(
    post_id: int,
    db: Session = Depends(get_db),
):
    delete_post(db=db, post_id=post_id)
