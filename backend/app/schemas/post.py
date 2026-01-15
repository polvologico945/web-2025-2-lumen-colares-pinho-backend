from typing import Optional, List
from pydantic import BaseModel, validator
from datetime import datetime

class PostBase(BaseModel):
    content: str

class PostCreate(PostBase):
    images: Optional[List[str]] = []  # URLs ou base64 das imagens
    
    @validator('images')
    def validate_images(cls, v):
        if v is None:
            return []
        
        # Validar quantidade máxima de imagens
        if len(v) > 5:
            raise ValueError('Máximo de 5 imagens por post')
        return v
    
    @validator('content')
    def validate_content(cls, v, values):
        if not v and not values.get('images'):
            raise ValueError('Post deve conter texto ou imagem')
        return v

class PostUpdate(BaseModel):
    content: Optional[str] = None
    images: Optional[List[str]] = None
    
    @validator('images')
    def validate_images(cls, v):
        if v is not None and len(v) > 5:
            raise ValueError('Máximo de 5 imagens por post')
        return v

class PostRead(PostBase):
    id: int
    user_id: int
    images: List[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True