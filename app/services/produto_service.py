from fastapi import HTTPException
from app.models.model_user import StatusPerfil
from sqlalchemy.orm import Session
from http import HTTPStatus
from app.models.product_model import Produto

def criar_produto_service(session: Session, produto_data: dict, current_user):
    if current_user.perfil != StatusPerfil.admin or not current_user.ativo:
        print(current_user.perfil)
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Somente usuario admin pode requisitar este servico"
        )
    
    existencia_produto = session.query(Produto).filter(Produto.codigo == produto_data['codigo']).first()
    if existencia_produto:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Produto ja existente"
        )
    
    produto = Produto(**produto_data)

    session.add(produto)
    session.commit()
    session.refresh(produto)
    return produto

def atualizar_completamente_service(produto_id: int, produto_data: dict, session: Session, current_user):
    if current_user.perfil != StatusPerfil.admin or not current_user.ativo:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Somente usuario admin pode requisitar esse servico"
        )
    
    produto = session.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Produto não encontrado"
        )
    
    produto.nome = produto_data['nome']
    produto.codigo = produto_data['codigo']
    produto.custo = produto_data['custo']
    produto.preco = produto_data['preco']
    produto.ativo = produto_data['ativo']

    session.commit()
    session.refresh(produto)

    return produto

def atualizar_parcialmente_service(produto_id: int, produto_data: dict, session: Session, current_user):
    if current_user.perfil != StatusPerfil.admin or not current_user.ativo:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Somente admin pode requisitar este servico"
        )
    
    produto = session.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Produto não encontrado"
        )
    
    for field, value in produto_data.items():
        setattr(produto, field, value)
    
    session.commit()
    session.refresh(produto)
    
    return produto