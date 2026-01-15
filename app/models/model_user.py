from sqlalchemy import Integer, String, Column, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
import enum

class StatusPerfil(enum.Enum):
    admin = 'admin'
    operador = 'operador'
    auditor = 'auditor'

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, index=True, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    perfil = Column(Enum(StatusPerfil), default=StatusPerfil.operador)
    ativo = Column(Boolean, nullable=False)