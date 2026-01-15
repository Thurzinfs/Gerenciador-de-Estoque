from pydantic import BaseModel, Field
from typing import Optional

class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    codigo: Optional[str] = None
    custo: Optional[float] = None
    preco: Optional[float] = None
    ativo: Optional[bool] = None
