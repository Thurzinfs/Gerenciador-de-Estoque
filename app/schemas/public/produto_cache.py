from pydantic import BaseModel

class ProdutoCachePublic(BaseModel):
    id: int
    nome: str
    quantidade: int