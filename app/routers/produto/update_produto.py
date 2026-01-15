from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from http import HTTPStatus
from app.models.product_model import Produto
from app.schemas.public.produto_public import ProdutoPublic
from app.schemas.schemas.produto_schemas import ProdutoSchema
from app.schemas.update.produto_update import ProdutoUpdate
from app.db.database import get_session
from app.core.security import get_current_user
from app.models.model_user import StatusPerfil
from app.services.produto_service import atualizar_completamente_service, atualizar_parcialmente_service

router = APIRouter(
    prefix='/api/produtos',
    tags=['api', 'produtos']
)

@router.put(
    path='/{produto_id}',
    response_model=ProdutoPublic,
    status_code=HTTPStatus.OK
)
def atualizar_produto(
    produto_id: int,
    data: ProdutoSchema,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    produto_data = data.model_dump()

    return atualizar_completamente_service(
        produto_id=produto_id,
        produto_data=produto_data,
        session=session,
        current_user=current_user
    )

@router.patch(
    path='/{produto_id}',
    response_model=ProdutoPublic,
    status_code=HTTPStatus.OK
)
def atualizar_parcialmente_produto(
    produto_id: int,
    data: ProdutoUpdate,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    produto_data = data.model_dump(exclude_unset=True)

    return atualizar_parcialmente_service(
        produto_id= produto_id,
        produto_data=produto_data,
        session=session,
        current_user=current_user
    )