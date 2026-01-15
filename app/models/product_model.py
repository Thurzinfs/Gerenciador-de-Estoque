from sqlalchemy import Column, String, Integer, Enum, Numeric, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base
import enum

class Produto(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    codigo = Column(String, nullable=False, unique=True)
    custo = Column(Numeric(10, 2), nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)
    ativo = Column(Boolean, nullable=False)
    estoque_atual = Column(Integer, default=0)

class StatusTipo(enum.Enum):
    entrada = "entrada"
    saida = "saida"
    ajuste = "ajuste"

class StatusOrigem(enum.Enum):
    compra = 'compra'
    venda = 'venda'
    perda = 'perda'
    devolucao = 'devolucao'

class Movimentacao(Base):
    __tablename__ = 'movimentacoes'
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(Enum(StatusTipo), default=StatusTipo.entrada)

    estoque_antes = Column(Integer, nullable=False)
    estoque_depois = Column(Integer, nullable=False)

    quantidade =Column(Integer, nullable=False)
    data = Column(DateTime, default=datetime.utcnow)
    origem = Column(Enum(StatusOrigem), default=StatusOrigem.compra)
    motivo = Column(String, nullable=True)
    referencia = Column(String, nullable=False)
    produto_id = Column(Integer, ForeignKey('produtos.id', ondelete="RESTRICT"), nullable=False)
    usuario_id = Column(Integer, ForeignKey('users.id', ondelete="RESTRICT"), nullable=False)
    
    produto = relationship('Produto')
    usuario = relationship('User')