from pydantic import BaseModel
from enum import Enum

class Perfil(str, Enum):
    admin = 'admin'
    operador = 'operador'
    auditor = 'auditor'

class userPublic(BaseModel):
    id: int
    nome: str
    email: str 
    password: str
    perfil: Perfil
    ativo: bool