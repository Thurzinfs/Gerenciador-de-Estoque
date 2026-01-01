# Sistema de Gerenciamento de Estoque

API desenvolvida com FastAPI para controle de produtos e movimentações de estoque.

## Tecnologias
- Python
- FastAPI
- SQLAlchemy
- SQLITE
- JWT

## Regras de Negócio
- Estoque só é alterado via movimentação
- Movimentações são imutáveis (POST / GET)
- Auditoria completa (quem, quando, motivo)
- Controle por perfil de usuário

## Como rodar
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
