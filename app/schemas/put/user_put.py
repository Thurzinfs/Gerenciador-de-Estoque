from pydantic import BaseModel
from enum import Enum

class Perfil(str, Enum):
    admin = 'admin'
    operador = 'operador'
    auditor = 'auditor'

class userPut(BaseModel):
    nome: str
    email: str 
    password: str
    perfil: Perfil
    ativo: bool