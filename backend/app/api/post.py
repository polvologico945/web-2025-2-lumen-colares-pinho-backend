from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
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
    content: str = Form(None),
    imagens: List[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cria um novo post.
    Suporta multipart/form-data para envio de texto (content) e imagens (imagens).
    """
    # Create schema from form data
    post_in = PostCreate(content=content or "")
    
    return create_post(db=db, post_in=post_in, user_id=current_user.id, files=imagens)


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


@router.get("/upload-limits")
def get_upload_limits():
    return {
        "sucesso": True,
        "limites": {
            "max_imagens": 5,
            "max_tamanho_mb": 5,
            "tipos_permitidos": ['jpg', 'jpeg', 'png', 'gif', 'webp'],
            "pasta_uploads": '/uploads'
        }
    }


@router.delete("/{post_id}", status_code=204)
def delete_post_endpoint(
    post_id: int,
    db: Session = Depends(get_db),
):
    delete_post(db=db, post_id=post_id)
