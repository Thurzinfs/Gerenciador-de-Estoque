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

class MovimentacaoPatch(BaseModel):
    tipo: Optional[Tipo] = None
    quantidade: Optional[int] = None
    data: Optional[datetime] = None
    origem: Optional[Origem] = None
    motivo: Optional[str] = None
    referencia: Optional[str] = None