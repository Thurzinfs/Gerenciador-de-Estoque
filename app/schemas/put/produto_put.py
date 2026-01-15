from pydantic import BaseModel, Field
from decimal import Decimal

class ProdutoPut(BaseModel):
    nome: str
    codigo: str
    custo: Decimal = Field(..., max_digits=10, decimal_places=2)
    preco: Decimal = Field(..., max_digits=10, decimal_places=2)
    ativo: bool
    estoque_atual: int 