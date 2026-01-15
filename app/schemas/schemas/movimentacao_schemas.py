from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class Tipo(str, Enum):
    entrada = "entrada"
    saida = "saida"
    ajuste = "ajuste"

class Origem(str, Enum):
    compra = 'compra'
    venda = 'venda'
    perda = 'perda'
    devolucao = 'devolucao'

class MovimentacaoSchema(BaseModel):
    tipo: Tipo
    quantidade: int
    data: datetime
    origem: Origem
    motivo: Optional[str] = None
    referencia: str
    produto_id: int
    usuario_id: int