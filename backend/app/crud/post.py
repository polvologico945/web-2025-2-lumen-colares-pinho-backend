from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
import os
from fastapi import UploadFile, HTTPException
import shutil

from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate

# Configurações
UPLOAD_DIR = "uploads/posts"
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_IMAGES_PER_POST = 5

def save_uploaded_files(files: List[UploadFile]) -> List[str]:
    """Salva arquivos enviados e retorna suas URLs"""
    
    # Garantir que o diretório existe
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    saved_files = []
    
    for file in files:
        # Validar extensão
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de arquivo não permitido: {file_ext}. Tipos permitidos: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Validar tamanho
        file_size = 0
        file.file.seek(0, 2)  # Ir para o final
        file_size = file.file.tell()
        file.file.seek(0)  # Resetar
        
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"Arquivo {file.filename} muito grande. Tamanho máximo: {MAX_FILE_SIZE//(1024*1024)}MB"
            )
        
        # Gerar nome único
        unique_filename = f"{uuid.uuid4().hex}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Salvar arquivo
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # URL para acesso
        file_url = f"/uploads/posts/{unique_filename}"
        saved_files.append(file_url)
    
    return saved_files

def create_post(db: Session, post_in: PostCreate, user_id: int, files: Optional[List[UploadFile]] = None) -> Post:
    """Cria um novo post com possíveis imagens"""
    
    image_urls = []
    
    # Se houver arquivos, salvá-los
    if files:
        # Validar quantidade
        if len(files) > MAX_IMAGES_PER_POST:
            raise HTTPException(
                status_code=400,
                detail=f"Máximo de {MAX_IMAGES_PER_POST} imagens por post"
            )
        
        image_urls = save_uploaded_files(files)
    
    # Se já houver URLs no post_in, adicionar também
    if post_in.images:
        image_urls.extend(post_in.images)
    
    # Validar total de imagens
    if len(image_urls) > MAX_IMAGES_PER_POST:
        raise HTTPException(
            status_code=400,
            detail=f"Máximo de {MAX_IMAGES_PER_POST} imagens por post. Você tentou enviar {len(image_urls)}"
        )
    
    # Validar que o post tem conteúdo ou imagens
    if not post_in.content and not image_urls:
        raise HTTPException(
            status_code=400,
            detail="Post deve conter texto ou imagem"
        )
    
    db_post = Post(
        content=post_in.content,
        user_id=user_id,
        images=image_urls
    )
    
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, post_id: int, post_in: PostUpdate, user_id: int, 
                new_files: Optional[List[UploadFile]] = None, 
                images_to_remove: Optional[List[str]] = None) -> Optional[Post]:
    """Atualiza um post existente"""
    
    db_post = db.query(Post).filter(Post.id == post_id, Post.user_id == user_id).first()
    if not db_post:
        return None
    
    # Atualizar conteúdo se fornecido
    if post_in.content is not None:
        db_post.content = post_in.content
    
    current_images = db_post.images or []
    
    # Remover imagens especificadas
    if images_to_remove:
        # Filtrar apenas as URLs que existem
        images_to_remove_set = set(images_to_remove)
        current_images = [img for img in current_images if img not in images_to_remove_set]
        
        # Opcional: deletar arquivos físicos
        for img_url in images_to_remove_set:
            if img_url.startswith("/uploads/posts/"):
                filename = img_url.split("/")[-1]
                file_path = os.path.join(UPLOAD_DIR, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
    
    # Adicionar novas imagens de arquivos
    new_image_urls = []
    if new_files:
        # Verificar espaço disponível
        available_slots = MAX_IMAGES_PER_POST - len(current_images)
        if len(new_files) > available_slots:
            raise HTTPException(
                status_code=400,
                detail=f"Limite de {MAX_IMAGES_PER_POST} imagens por post. "
                      f"Você pode adicionar no máximo {available_slots} imagem(ns)"
            )
        
        new_image_urls = save_uploaded_files(new_files)
        current_images.extend(new_image_urls)
    
    # Adicionar URLs do post_in se fornecidas
    if post_in.images is not None:
        current_images.extend(post_in.images)
    
    # Validar total final
    if len(current_images) > MAX_IMAGES_PER_POST:
        raise HTTPException(
            status_code=400,
            detail=f"Máximo de {MAX_IMAGES_PER_POST} imagens por post"
        )
    
    db_post.images = current_images
    db.commit()
    db.refresh(db_post)
    return db_post

# Mantenha as outras funções como estão
def get_post(db: Session, post_id: int) -> Optional[Post]:
    return db.query(Post).filter(Post.id == post_id).first()

def list_posts(db: Session, skip: int = 0, limit: int = 100) -> List[Post]:
    return db.query(Post).order_by(Post.created_at.desc()).offset(skip).limit(limit).all()

def delete_post(db: Session, post_id: int, user_id: int) -> bool:
    """Deleta um post e suas imagens associadas"""
    db_post = db.query(Post).filter(Post.id == post_id, Post.user_id == user_id).first()
    if not db_post:
        return False
    
    # Deletar arquivos físicos das imagens
    if db_post.images:
        for img_url in db_post.images:
            if img_url.startswith("/uploads/posts/"):
                filename = img_url.split("/")[-1]
                file_path = os.path.join(UPLOAD_DIR, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
    
    db.delete(db_post)
    db.commit()
    return True