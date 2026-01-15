from pydantic import BaseModel
from enum import Enum

class Perfil(str, Enum):
    operador = 'operador'
    admin = 'admin'
    auditor = 'auditor'

class userSchema(BaseModel):
    nome: str
    email: str 
    password: str
    perfil: Perfil
    ativo: bool