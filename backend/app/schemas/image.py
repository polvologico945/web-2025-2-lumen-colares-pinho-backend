from pydantic import BaseModel, validator
from typing import List, Optional
from fastapi import UploadFile, File
import magic

class ImageUpload(BaseModel):
    files: List[UploadFile]
    
    @validator('files')
    def validate_files(cls, v):
        # Validar quantidade
        if len(v) > 5:
            raise ValueError('Máximo de 5 imagens por post')
        
        # Validar cada arquivo
        for i, file in enumerate(v):
            # Validar tipo MIME
            mime_type = magic.from_buffer(file.file.read(1024), mime=True)
            file.file.seek(0)  # Resetar ponteiro do arquivo
            
            allowed_mimes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            if mime_type not in allowed_mimes:
                raise ValueError(f'Imagem {i+1}: Tipo de arquivo não permitido. Tipos permitidos: JPEG, PNG, GIF, WebP')
            
            # Validar tamanho (máx 5MB)
            MAX_SIZE = 5 * 1024 * 1024  # 5MB
            file.file.seek(0, 2)  # Ir para o final
            file_size = file.file.tell()
            file.file.seek(0)  # Resetar
            
            if file_size > MAX_SIZE:
                raise ValueError(f'Imagem {i+1}: Tamanho máximo de 5MB excedido')
        
        return v

class ImageResponse(BaseModel):
    url: str
    filename: str
    size: int
    mime_type: str