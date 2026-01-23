from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.pedido import PedidoAjuda, PedidoComentario
from app.schemas.pedido import PedidoCreate, PedidoComentarioCreate
from datetime import datetime

def create_pedido(db: Session, pedido: PedidoCreate, user_id: int):
    db_pedido = PedidoAjuda(
        titulo=pedido.titulo,
        descricao=pedido.descricao,
        materia=pedido.materia,
        user_id=user_id,
        status="pendente",
        created_at=datetime.utcnow()
    )
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

def get_pedidos(db: Session, skip: int = 0, limit: int = 100, status: str = None):
    query = db.query(PedidoAjuda)
    if status and status != "todos":
        query = query.filter(PedidoAjuda.status == status)
    return query.order_by(desc(PedidoAjuda.created_at)).offset(skip).limit(limit).all()

def get_pedidos_by_user(db: Session, user_id: int):
    # Pedidos criados pelo usuário ou aceitos por ele
    return db.query(PedidoAjuda).filter(
        (PedidoAjuda.user_id == user_id) | (PedidoAjuda.accepted_by_id == user_id)
    ).order_by(desc(PedidoAjuda.created_at)).all()

def get_pedido(db: Session, pedido_id: int):
    return db.query(PedidoAjuda).filter(PedidoAjuda.id == pedido_id).first()

def aceitar_pedido(db: Session, pedido: PedidoAjuda, user_id: int):
    pedido.status = "aceito"
    pedido.accepted_by_id = user_id
    pedido.accepted_at = datetime.utcnow()
    db.commit()
    db.refresh(pedido)
    return pedido

def concluir_pedido(db: Session, pedido: PedidoAjuda):
    pedido.status = "concluído"
    pedido.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(pedido)
    return pedido

def create_comentario(db: Session, comentario: PedidoComentarioCreate, pedido_id: int, user_id: int):
    db_comentario = PedidoComentario(
        content=comentario.conteudo,
        pedido_id=pedido_id,
        user_id=user_id,
        created_at=datetime.utcnow()
    )
    db.add(db_comentario)
    db.commit()
    db.refresh(db_comentario)
    return db_comentario
