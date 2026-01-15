from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum
from app.schemas.public.produto_public import ProdutoPublic
from app.schemas.public.user_public import userPublic

class Tipo(str, Enum):
    entrada = "entrada"
    saida = "saida"
    ajuste = "ajuste"

class Origem(str, Enum):
    compra = 'compra'
    venda = 'venda'
    perda = 'perda'
    devolucao = 'devolucao'

class MovimentacaoPublic(BaseModel):
    id: int
    tipo: Tipo
    quantidade: int
    estoque_antes: int
    estoque_depois: int
    data: datetime
    origem: Origem
    motivo: Optional[str] = None
    referencia: str
    produto_id: int
    usuario_id: int
    produto: ProdutoPublic
    usuario: userPublic