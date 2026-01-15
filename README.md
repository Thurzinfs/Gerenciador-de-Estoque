# Sistema de Gerenciamento de Estoque

API RESTful para controle inteligente de produtos e movimentações de estoque, desenvolvida com FastAPI, SQLAlchemy e autenticação JWT.

## 📋 Visão Geral

Sistema completo de gerenciamento de estoque com suporte a múltiplos usuários, controle de acesso por perfil e auditoria completa de todas as movimentações. O sistema implementa regras de negócio rigorosas para garantir integridade e rastreabilidade total das transações.

## 🛠️ Tecnologias

- **Backend**: FastAPI 0.128.0
- **ORM**: SQLAlchemy 2.0.45
- **Banco de Dados**: SQLite
- **Autenticação**: JWT (PyJWT 2.10.1)
- **Hash de Senha**: Argon2 (argon2-cffi 25.1.0)
- **Validação**: Pydantic 2.12.5
- **Python**: ≥3.11

## 📦 Instalação e Configuração

### Pré-requisitos
- Python 3.11+
- `uv` (gerenciador de pacotes recomendado) ou `pip`

### Sobre o `uv`

`uv` é um gerenciador de pacotes Python moderno e ultra-rápido, escrito em Rust. Oferece:
- ⚡ **Instalação 10-100x mais rápida** que pip
- 🔒 **Resolução de dependências confiável** com lock file (`uv.lock`)
- 📦 **Suporte a pyproject.toml** como este projeto
- 🌍 **Compatibilidade com pip e pip-tools**

Para instalar `uv`:
```PowerShell
irm https://astral.sh/uv/install.ps1 | iex
# Ou via cargo (Rust)
cargo install uv
```

### Passos de Instalação

1. **Clonar/Acessar o projeto**
```bash
cd "Gerenciador Inteligente/backend"
```

2. **Instalar dependências**

**Opção A: Usando `uv` (recomendado)**
```bash
# Instala as dependências do pyproject.toml e gera/usa uv.lock
uv sync

# Se precisar adicionar uma nova dependência
uv add nome-do-pacote

# Ou remover
uv remove nome-do-pacote
```

**Opção B: Usando `pip`**
```bash
pip install -r requeriments.txt
```

3. **Configurar variáveis de ambiente**

Criar arquivo `.env` na raiz do projeto:
```env
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=sua_chave_secreta_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

4. **Iniciar o servidor**

```bash
# Com uv
uv run uvicorn app.main:app --reload

# Ou diretamente
uvicorn app.main:app --reload
```

O servidor estará disponível em: `http://localhost:8000`

## 📚 Estrutura do Projeto

```
backend/
├── app/
│   ├── core/                    # Configurações e segurança
│   │   ├── config.py            # Variáveis de ambiente
│   │   ├── security.py          # JWT e hash de senha
│   │   └── exceptions.py        # Handlers de exceção
│   ├── crud/                    # Operações CRUD de usuários
│   │   ├── user_post.py         # Criar usuário
│   │   ├── user_get.py          # Listar/obter usuário
│   │   ├── user_patch.py        # Atualizar parcial
│   │   ├── user_put.py          # Atualizar completo
│   │   └── user_delete.py       # Deletar usuário
│   ├── db/
│   │   └── database.py          # Conexão e sessão do BD
│   ├── models/                  # Modelos SQLAlchemy
│   │   ├── model_user.py        # Modelo de usuário
│   │   └── product_model.py     # Modelos de produto e movimentação
│   ├── routers/                 # Rotas da API
│   │   ├── auth_user.py         # Autenticação (login)
│   │   ├── list_users.py        # Listar usuários
│   │   ├── produto/             # Rotas de produtos
│   │   │   ├── post_produto.py  # Criar produto
│   │   │   ├── get_produto.py   # Obter produto
│   │   │   └── update_produto.py# Atualizar produto
│   │   └── movimentacao/        # Rotas de movimentações
│   │       └── router_movimentacao.py
│   ├── schemas/                 # Pydantic schemas para validação
│   │   ├── public/              # Schemas para respostas públicas
│   │   ├── schemas/             # Schemas de request
│   │   ├── token/               # Schemas de autenticação
│   │   ├── put/                 # Schemas para PUT
│   │   └── update/              # Schemas para UPDATE
│   ├── services/                # Lógica de negócio
│   │   ├── user_services.py     # Serviços de usuário
│   │   ├── produto_service.py   # Serviços de produto
│   │   └── movimentacao_service.py # Serviços de movimentação
│   └── main.py                  # App FastAPI e rotas
├── main.py                      # Entry point
├── pyproject.toml               # Configuração do projeto
├── requeriments.txt             # Dependências Python
└── README.md                    # Este arquivo
```

## 🔐 Segurança e Autenticação

### Perfis de Usuário

O sistema suporta 3 tipos de perfis:

| Perfil | Descrição | Permissões |
|--------|-----------|-----------|
| **admin** | Administrador | Todas as operações (CRUD de usuários, produtos, movimentações e auditoria) |
| **operador** | Operador | Permissão limitada (não pode criar/modificar produtos ou movimentações) |
| **auditor** | Auditor | Apenas leitura de relatórios e históricos |

### Fluxo de Autenticação

1. Usuário faz login com email e senha em `/auth/token`
2. Sistema valida credenciais e retorna JWT
3. Token deve ser incluído no header `Authorization: Bearer <token>` para requisições autenticadas
4. Token expira conforme `ACCESS_TOKEN_EXPIRE_MINUTES`

### Hashing de Senha

Senhas são hasheadas com Argon2, garantindo segurança mesmo em caso de exposição do banco de dados.

## 📊 Regras de Negócio

### Estoque e Movimentações

- ✅ **Estoque imutável**: O estoque atual de produtos **nunca** é alterado diretamente; toda alteração é feita através de movimentações
- ✅ **Movimentações imutáveis**: Uma vez criada, uma movimentação não pode ser alterada (apenas GET/POST)
- ✅ **Auditoria completa**: Cada movimentação registra:
  - Usuário responsável
  - Data e hora exata
  - Estoque antes e depois
  - Tipo de movimento
  - Origem (compra, venda, perda, devolução)
  - Motivo (especialmente para ajustes)
  - Referência externa

### Tipos de Movimentação

| Tipo | Descrição | Impacto |
|------|-----------|--------|
| **entrada** | Produto entra em estoque | Aumenta estoque |
| **saída** | Produto sai de estoque | Diminui estoque |
| **ajuste** | Correção de inventário (requer motivo) | Aumenta ou diminui |

### Origens de Movimentação

- `compra` - Entrada por compra
- `venda` - Saída por venda
- `perda` - Saída por perda/dano
- `devolução` - Entrada por devolução

### Validações

- ❌ Não é possível criar movimentação com quantidade ≤ 0
- ❌ Não é possível deixar estoque negativo
- ❌ Movimentação de ajuste **obrigatoriamente** requer motivo
- ❌ Produto não pode ter dois códigos iguais
- ❌ Apenas admins podem criar/modificar produtos
- ❌ Apenas admins podem registrar movimentações

## 🔌 Endpoints da API

### Autenticação

#### Login
```http
POST /auth/token
Content-Type: application/x-www-form-urlencoded

username=usuario@email.com&password=senha123
```

**Resposta (200 OK)**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "Bearer"
}
```

### Usuários

#### Criar Usuário (POST)
```http
POST /api/users
Authorization: Bearer <token>
Content-Type: application/json

{
  "nome": "João Silva",
  "email": "joao@example.com",
  "password": "senha123",
  "perfil": "operador",
  "ativo": true
}
```

#### Listar Usuários (GET)
```http
GET /api/users
Authorization: Bearer <token>
```

#### Obter Usuário por ID (GET)
```http
GET /api/users/{id}
Authorization: Bearer <token>
```

#### Atualizar Usuário Completo (PUT)
```http
PUT /api/users/{id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "nome": "João Silva Atualizado",
  "email": "novo@example.com",
  "password": "novaSenha123",
  "perfil": "admin",
  "ativo": true
}
```

#### Atualizar Usuário Parcialmente (PATCH)
```http
PATCH /api/users/{id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "nome": "Novo Nome"
}
```

#### Deletar Usuário (DELETE)
```http
DELETE /api/users/{id}
Authorization: Bearer <token>
```

### Produtos

#### Criar Produto (POST)
```http
POST /api/produtos
Authorization: Bearer <token> (requer perfil admin)
Content-Type: application/json

{
  "nome": "Notebook Dell",
  "codigo": "NB-DELL-001",
  "custo": 2500.00,
  "preco": 3500.00,
  "ativo": true
}
```

#### Obter Produto por ID (GET)
```http
GET /api/produtos/{produto_id}
```

**Resposta**
```json
{
  "id": 1,
  "nome": "Notebook Dell",
  "quantidade": 5
}
```

#### Atualizar Produto (PUT)
```http
PUT /api/produtos/{produto_id}
Authorization: Bearer <token> (requer perfil admin)
Content-Type: application/json

{
  "nome": "Notebook Dell XPS",
  "codigo": "NB-DELL-XPS-001",
  "custo": 2700.00,
  "preco": 3700.00,
  "ativo": true
}
```

### Movimentações

#### Registrar Movimentação (POST)
```http
POST /api/movimentacoes
Authorization: Bearer <token> (requer perfil admin)
Content-Type: application/json

{
  "tipo": "entrada",
  "quantidade": 10,
  "origem": "compra",
  "motivo": null,
  "referencia": "NF-2026-001",
  "produto_id": 1,
  "usuario_id": 1
}
```

**Resposta (201 Created)**
```json
{
  "id": 1,
  "tipo": "entrada",
  "estoque_antes": 0,
  "estoque_depois": 10,
  "quantidade": 10,
  "data": "2026-01-14T10:30:00",
  "origem": "compra",
  "motivo": null,
  "referencia": "NF-2026-001",
  "produto_id": 1,
  "usuario_id": 1
}
```

#### Listar Todas as Movimentações (GET)
```http
GET /api/movimentacoes/movimentacoes
Authorization: Bearer <token> (requer perfil admin)
```

#### Listar Movimentações por Produto (GET)
```http
GET /api/movimentacoes/produto/{produto_id}/movimentacao
Authorization: Bearer <token> (requer perfil admin)
```

## 🧪 Exemplos de Uso

### Fluxo Completo

1. **Login**
```bash
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=admin123"
```

2. **Criar Produto**
```bash
curl -X POST "http://localhost:8000/api/produtos" \
  -H "Authorization: Bearer <seu_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Mouse Logitech",
    "codigo": "MOUSE-LOG-001",
    "custo": 30.00,
    "preco": 80.00,
    "ativo": true
  }'
```

3. **Registrar Entrada de Estoque**
```bash
curl -X POST "http://localhost:8000/api/movimentacoes" \
  -H "Authorization: Bearer <seu_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "entrada",
    "quantidade": 50,
    "origem": "compra",
    "motivo": null,
    "referencia": "NF-2026-0001",
    "produto_id": 1,
    "usuario_id": 1
  }'
```

4. **Consultar Estoque**
```bash
curl -X GET "http://localhost:8000/api/produtos/1"
```

## 🚀 Deployment

### Usando Uvicorn (Produção)

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Com Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

## 📝 Notas Importantes

- O banco de dados é criado automaticamente na primeira execução
- Todas as operações críticas requerem autenticação JWT
- Operações de escrita de estoque requerem perfil **admin**
- Variáveis de ambiente em `.env` sobrescrevem defaults
- Logs de erro completos estão disponíveis no console

## 📄 Licença

Este projeto é propriedade privada.
