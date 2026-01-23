import os
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    ForeignKey,
    JSON
)
from sqlalchemy.orm import relationship
from app.db.base import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Relacionamentos
    user = relationship("User", back_populates="posts")
    comments = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan"
    )
    likes = relationship(
        "Like",
        back_populates="post",
        cascade="all, delete-orphan"
    )

    # Imagens (lista de URLs)
    images = Column(JSON, default=list)

    # Configurações
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    MAX_IMAGES_PER_POST = 5
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

    
    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "user_id": self.user_id,
            "user": self.user.to_dict() if self.user else None,
            "images": self.images or [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "comments_count": len(self.comments) if self.comments else 0,
            "likes_count": len(self.likes) if self.likes else 0,
        }

    
    @staticmethod
    def allowed_file(filename: str) -> bool:
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower()
            in Post.ALLOWED_EXTENSIONS
        )

    
    @staticmethod
    def validate_image(file):
        if not file or file.filename == "":
            return False, "Nenhum arquivo selecionado"

        if not Post.allowed_file(file.filename):
            return (
                False,
                f"Tipo de arquivo não permitido. "
                f"Tipos permitidos: {', '.join(Post.ALLOWED_EXTENSIONS)}"
            )

        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)

        if file_size > Post.MAX_FILE_SIZE:
            return (
                False,
                f"Arquivo muito grande. "
                f"Tamanho máximo: {Post.MAX_FILE_SIZE // (1024 * 1024)}MB"
            )

        return True, "OK"


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relacionamentos
    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relacionamentos
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")
