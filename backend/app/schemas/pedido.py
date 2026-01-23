from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.schemas.user import UserRead

class PedidoComentarioCreate(BaseModel):
    conteudo: str

class PedidoComentarioRead(BaseModel):
    id: int
    content: str = Field(serialization_alias="conteudo")
    autor: UserRead
    created_at: datetime = Field(serialization_alias="data")

    class Config:
        from_attributes = True

class PedidoBase(BaseModel):
    titulo: str
    descricao: str
    materia: str

class PedidoCreate(PedidoBase):
    pass

class PedidoRead(PedidoBase):
    id: int
    status: str
    created_at: datetime = Field(serialization_alias="dataCriacao")
    accepted_at: Optional[datetime] = Field(None, serialization_alias="dataAceito")
    completed_at: Optional[datetime] = Field(None, serialization_alias="dataConclusao")
    
    autor: UserRead
    aceito_por: Optional[UserRead] = Field(None, serialization_alias="aceitoPor")
    comentarios: List[PedidoComentarioRead] = []

    class Config:
        from_attributes = True
        populate_by_name = True

