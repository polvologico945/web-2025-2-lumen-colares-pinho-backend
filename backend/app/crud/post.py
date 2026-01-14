from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate


def get_post(db: Session, post_id: int) -> Optional[Post]:
    return db.query(Post).filter(Post.id == post_id).first()


def list_posts(db: Session, skip: int = 0, limit: int = 100) -> List[Post]:
    return db.query(Post).offset(skip).limit(limit).all()


def create_post(db: Session, post_in: PostCreate) -> Post:
    db_post = Post(
        conteudo=post_in.conteudo,
        data_criacao=datetime.utcnow(),
        author_id=post_in.author_id,
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(
    db: Session, post_id: int, post_in: PostUpdate
) -> Optional[Post]:
    db_post = get_post(db, post_id)
    if not db_post:
        return None

    data = post_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(db_post, field, value)

    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: int) -> None:
    db.query(Post).filter(Post.id == post_id).delete()
    db.commit()
