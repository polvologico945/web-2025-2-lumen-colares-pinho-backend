import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app
from app.models import Post

def save_uploaded_file(file):
    """Salva um único arquivo e retorna sua URL"""
    if not file or not file.filename:
        return None
    
    # Validar
    is_valid, message = Post.validate_image(file)
    if not is_valid:
        raise ValueError(message)
    
    # Gerar nome único
    original_filename = secure_filename(file.filename)
    file_ext = original_filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{file_ext}"
    
    # Garantir diretório
    upload_folder = os.path.join(current_app.root_path, '..', 'uploads', 'posts')
    os.makedirs(upload_folder, exist_ok=True)
    
    # Salvar
    file_path = os.path.join(upload_folder, unique_filename)
    file.save(file_path)
    
    # Retornar URL
    return f"/uploads/posts/{unique_filename}"

def validate_images(files, max_count=5):
    """Valida uma lista de arquivos de imagem"""
    errors = []
    
    if len(files) > max_count:
        errors.append(f'Máximo de {max_count} imagens permitido')
    
    for i, file in enumerate(files):
        if file and file.filename:
            is_valid, message = Post.validate_image(file)
            if not is_valid:
                errors.append(f'Imagem {i+1}: {message}')
    
    return errors