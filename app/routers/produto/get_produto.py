from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.product_model import Produto
from app.schemas.public.produto_public import ProdutoPublic
from app.schemas.public.produto_cache import ProdutoCachePublic
from app.db.database import get_session
from http import HTTPStatus

router = APIRouter(
    prefix='/api/produtos',
    tags=['api', 'produtos']
)

@router.get(
    path='/{produto_id}',
    response_model=ProdutoCachePublic,
    status_code=HTTPStatus.OK
)
def pegar_produto(
    produto_id: int,
    session: Session = Depends(get_session)
):
    produto = session.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Produto not found'
        )
    
    produto_return = {
        'id' : produto.id,
        'nome' : produto.nome,
        'quantidade' : produto.estoque_atual
    }
    
    return produto_return
