from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session
from app.models.product_model import Produto
from app.schemas.public.produto_public import ProdutoPublic
from app.schemas.schemas.produto_schemas import ProdutoSchema
from app.db.database import get_session
from app.core.security import get_current_user
from app.models.model_user import StatusPerfil
from app.services.produto_service import criar_produto_service

router = APIRouter(
    prefix='/api/produtos',
    tags=['api', 'produtos']
)

@router.post(
    path='/',
    response_model=ProdutoPublic,
    status_code=HTTPStatus.CREATED
)
def cadastrar_produto(
    data: ProdutoSchema,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    produto_data = data.model_dump()
    return criar_produto_service(
        session = session,
        produto_data = produto_data,
        current_user = current_user
    )
