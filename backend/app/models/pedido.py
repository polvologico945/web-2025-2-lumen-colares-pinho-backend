from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class PedidoAjuda(Base):
    __tablename__ = "pedidos_ajuda"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(Text, nullable=False)
    materia = Column(String, nullable=False)
    status = Column(String, default="pendente")  # pendente, aceito, concluído
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    accepted_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    accepted_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # Relacionamentos
    autor = relationship("User", foreign_keys=[user_id], back_populates="pedidos")
    aceito_por = relationship("User", foreign_keys=[accepted_by_id], back_populates="pedidos_aceitos")
    
    comentarios = relationship("PedidoComentario", back_populates="pedido", cascade="all, delete-orphan")

class PedidoComentario(Base):
    __tablename__ = "pedido_comentarios"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    pedido_id = Column(Integer, ForeignKey("pedidos_ajuda.id"), nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relacionamentos
    autor = relationship("User")
    pedido = relationship("PedidoAjuda", back_populates="comentarios")
