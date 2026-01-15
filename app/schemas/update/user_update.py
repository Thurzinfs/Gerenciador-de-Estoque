from pydantic import BaseModel
from typing import Optional
from enum import Enum

class Perfil(str, Enum):
    admin = 'admin'
    operador = 'operador'
    auditor = 'auditor'

class userUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    perfil: Optional[Perfil] = None
    ativo: Optional[bool] = None