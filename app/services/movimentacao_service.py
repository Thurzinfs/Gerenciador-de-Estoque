from sqlalchemy.orm import Session
from http import HTTPStatus
from fastapi import HTTPException
from app.models.product_model import Movimentacao, Produto
from app.schemas.schemas.movimentacao_schemas import MovimentacaoSchema, Tipo
from app.models.model_user import StatusPerfil

def registrar_movimentacao(
    movimentacao: MovimentacaoSchema,
    session: Session,
    current_user
):
    movimentacao = Movimentacao(**movimentacao.model_dump())
    produto = session.query(Produto).filter(Produto.id == movimentacao.produto_id).first()

    if not produto:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Produto not found")
    
    if current_user.perfil != StatusPerfil.admin or not current_user.ativo:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="somente usuario admin pode executar este recurso")
    
    if movimentacao.quantidade <= 0:
        raise HTTPException(status_code=HTTPStatus.INSUFFICIENT_STORAGE, detail="Quantidade invalida")
    
    try:
        cache = 0

        if movimentacao.tipo == Tipo.entrada:
            cache = movimentacao.quantidade
            
        elif movimentacao.tipo == Tipo.saida:
            cache = -movimentacao.quantidade
            
        elif movimentacao.tipo == Tipo.ajuste:
            if not movimentacao.motivo:
                raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Sem motivo para esta transacao")
            
            cache = movimentacao.quantidade

        estoque_antes = produto.estoque_atual
        estoque_depois = estoque_antes + cache

        if estoque_depois < 0:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="quantidade de estoque insuficiente pra transacao")
        
        produto.estoque_atual =  estoque_depois

        movimentacao.estoque_antes = estoque_antes
        movimentacao.estoque_depois = estoque_depois
        
        session.add(produto)
        session.add(movimentacao)

        session.commit()
        session.refresh(produto)
        session.refresh(movimentacao)
        return movimentacao
    
    except:
        session.rollback()
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error from server")

def listar_movimentacao(session: Session, current_user):
    if current_user.perfil != StatusPerfil.admin or not current_user.ativo:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Somente usuario admin pode executar este recurso")
    
    movimentacao = session.query(Movimentacao).order_by(Movimentacao.data.desc()).all()
    return movimentacao
    
def listar_movimentacao_produto(produto_id: int, session: Session,current_user):
    if current_user.perfil != StatusPerfil.admin or not current_user.ativo:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Somente usuario admin pode executar este recurso")
    
    movimentacao_produto = session.query(Movimentacao).filter(Movimentacao.produto_id == produto_id).order_by(Movimentacao.data.desc()).all()
    return movimentacao_produto
