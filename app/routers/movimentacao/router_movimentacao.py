from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session
from app.models.product_model import Produto, Movimentacao, StatusOrigem, StatusTipo
from app.models.model_user import StatusPerfil
from app.db.database import get_session
from app.schemas.public.movimentacao_public import MovimentacaoPublic
from app.schemas.schemas.movimentacao_schemas import MovimentacaoSchema
from app.core.security import get_current_user
from app.services.movimentacao_service import registrar_movimentacao, listar_movimentacao, listar_movimentacao_produto
from typing import List

router = APIRouter(prefix='/api/movimentacoes', tags=['api', 'movimentacoes'])

@router.post(
    path='/',
    response_model=MovimentacaoPublic,
    status_code=HTTPStatus.CREATED
)
def criar_movimentacao(
    data: MovimentacaoSchema,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    return registrar_movimentacao(
        movimentacao=data,
        session=session,
        current_user=current_user
    )

@router.get(
    path='/movimentacoes',
    response_model=List[MovimentacaoPublic],
)
def pegar_movimentacao_rapida(
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    return listar_movimentacao(
        session=session,
        current_user=current_user
    )

@router.get(
    path='/produto/{produto_id}/movimentacao',
    response_model=List[MovimentacaoPublic],
)
def movimentacao_produto(
    produto_id: int,
    session : Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    return listar_movimentacao_produto(
        produto_id=produto_id,
        session=session,
        current_user=current_user
    )