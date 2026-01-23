from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.pedido import PedidoCreate, PedidoRead, PedidoComentarioCreate, PedidoComentarioRead
from app.crud import pedido as crud_pedido

router = APIRouter()

@router.post("/", response_model=PedidoRead, status_code=status.HTTP_201_CREATED)
def create_pedido(
    pedido_in: PedidoCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud_pedido.create_pedido(db=db, pedido=pedido_in, user_id=current_user.id)

@router.get("/", response_model=List[PedidoRead])
def read_pedidos(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    db: Session = Depends(get_db)
):
    return crud_pedido.get_pedidos(db=db, skip=skip, limit=limit, status=status)

@router.get("/meus", response_model=List[PedidoRead])
def read_my_pedidos(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud_pedido.get_pedidos_by_user(db=db, user_id=current_user.id)

@router.put("/{pedido_id}/aceitar", response_model=PedidoRead)
def aceitar_pedido_endpoint(
    pedido_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    pedido = crud_pedido.get_pedido(db=db, pedido_id=pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    if pedido.user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Você não pode aceitar seu próprio pedido")
    if pedido.status != "pendente":
        raise HTTPException(status_code=400, detail=f"Pedido já está {pedido.status}")
    
    return crud_pedido.aceitar_pedido(db=db, pedido=pedido, user_id=current_user.id)

@router.put("/{pedido_id}/concluir", response_model=PedidoRead)
def concluir_pedido_endpoint(
    pedido_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    pedido = crud_pedido.get_pedido(db=db, pedido_id=pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    # Apenas autor ou quem aceitou pode concluir
    is_owner = pedido.user_id == current_user.id
    is_helper = pedido.accepted_by_id == current_user.id
    
    if not (is_owner or is_helper):
        raise HTTPException(status_code=403, detail="Permissão negada")
    
    return crud_pedido.concluir_pedido(db=db, pedido=pedido)

@router.post("/{pedido_id}/comentarios", response_model=PedidoComentarioRead, status_code=status.HTTP_201_CREATED)
def create_comment_endpoint(
    pedido_id: int,
    comentario: PedidoComentarioCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    pedido = crud_pedido.get_pedido(db=db, pedido_id=pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
        
    return crud_pedido.create_comentario(db=db, comentario=comentario, pedido_id=pedido_id, user_id=current_user.id)
