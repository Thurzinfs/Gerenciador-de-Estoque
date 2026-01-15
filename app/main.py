from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.crud.user_post import post_router
from app.crud.user_get import get_router
from app.crud.user_patch import patch_router
from app.crud.user_put import put_router
from app.crud.user_delete import delete_router
from app.routers.auth_user import auth_router
from app.db.database import Base, engine
from app.routers.list_users import routers
from sqlalchemy.exc import IntegrityError
from app.core.exceptions import Integrit_error_handler

from app.routers.produto.post_produto import router as post_produto
from app.routers.produto.get_produto import router as get_produto
from app.routers.produto.update_produto import router as update_produto

from app.routers.movimentacao.router_movimentacao import router as router_movimentacao

app = FastAPI(
    title="Gerenciamento de Estoque",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_headers=["*"]
)
app.add_exception_handler(
    IntegrityError,
    Integrit_error_handler
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"msg" : "OK"}

app.include_router(post_router)
app.include_router(get_router)
app.include_router(patch_router)
app.include_router(put_router)
app.include_router(delete_router)
app.include_router(auth_router)
app.include_router(routers)
app.include_router(post_produto)
app.include_router(get_produto)
app.include_router(update_produto)
app.include_router(router_movimentacao)
