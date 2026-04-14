# 🔧 Natural Organic Store - Backend API

## 📋 Sobre o Projeto

API RESTful desenvolvida em Python com FastAPI para gerenciar uma loja virtual de produtos orgânicos. Sistema completo de e-commerce com integração a APIs externas de geolocalização e endereços.

## Vídeo de Apresentação do Projeto Final | Disciplina: Back-end Avançado | PUC-Rio

[![Assista ao vídeo](https://img.youtube.com/vi/cqKe0fkphVE/0.jpg)](https://www.youtube.com/watch?v=cqKe0fkphVE)

### ✨ Funcionalidades

- 🛒 **Carrinho de Compras**: CRUD completo
- 📦 **Produtos**: Catálogo com imagens múltiplas
- 📍 **Geolocalização**: Busca de lojas próximas por CEP
- 🗺️ **Rotas**: Cálculo de distância e traçado de rotas
- ⭐ **Favoritos**: Sistema de lojas favoritas do usuário
- 📊 **PostgreSQL**: Persistência de dados relacional
- 📖 **Swagger**: Documentação interativa automática

---

## 🚀 Tecnologias

- **Python 3.11**
- **FastAPI 0.109** - Framework web moderno
- **SQLAlchemy 2.0** - ORM para banco de dados
- **PostgreSQL 15** - Banco relacional
- **Pydantic 2.5** - Validação de dados
- **Uvicorn 0.27** - Servidor ASGI
- **Geopy 2.4** - Cálculos geoespaciais

---

## 📦 Instalação

### Pré-requisitos
- Python 3.11+
- PostgreSQL 15+ (ou Docker)
- Chaves de API:
  - Geoapify (https://www.geoapify.com/)

###  Opção 1: Com Docker Compose (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/ledelmastro/natural-organic-frontend.git
cd..

# Clone o repositório
git clone https://github.com/ledelmastro/natural-organic-backend.git
cd natural-organic-frontend

# Configurar variáveis de ambiente
# Copie o arquivo de exemplo:
cp .env.example .env


# ⚠️ E configure:

GEOAPIFY_API_KEY
VITE_WEATHER_API_KEY
DATABASE_URL

# Build e execute o container
docker-compose up -d --build

# Acesse http://localhost:3000
```

### Opção 2: Desenvolvimento Local

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env .env

# Executar a aplicação
uvicorn main:app --reload --port 8000

# Acessar documentação
# http://localhost:8000/docs
```

---

## 🗂️ Estrutura do Projeto
```text
natural-organic-backend/
├── app/                        # Lógica central da aplicação
│   ├── routers/                # Divisão de rotas por funcionalidade
│   │   ├── __init__.py
│   │   ├── carrinho.py
│   │   ├── geolocalizacao.py
│   │   └── produtos.py
│   ├── __init__.py
│   ├── models.py               # Definições das tabelas do banco
│   └── schemas.py              # Pydantic (Validação/Serialização)
├── docs/                       # Documentação e imagens do projeto
│   ├── image.png
│   └── swagger.png
├── .dockerignore
├── .env                        # Variáveis de ambiente
├── .gitignore
├── database.py                 # Configuração de conexão com o banco
├── Dockerfile                  # Configuração da imagem Docker
├── main.py                     # Entry point (onde FastAPI é instanciado)
├── README.md
└── requirements.txt            # Dependências do Python


### Organização do Código (main.py)

```python
# Modelos do Banco (SQLAlchemy)
- UnidadeFisicaDB      # Lojas físicas
- FavoritoDB           # Favoritos do usuário
- CarrinhoDB           # Itens do carrinho
- ProdutoDB            # Catálogo de produtos

# Schemas (Pydantic)
- BuscaCEPRequest
- FavoritoRequest
- ItemCarrinho
- ProdutoCreate

# Rotas
- /carrinho/*          # CRUD carrinho
- /produtos/*          # CRUD produtos
- /geolocalizacao/*    # Busca e favoritos
- /docs                # Swagger
```

---

## 🌐 Endpoints da API

### 🛒 Carrinho de Compras

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/carrinho` | Lista todos os itens |
| POST | `/carrinho` | Adiciona item |
| PUT | `/carrinho/{id}?quantidade=N` | Atualiza quantidade |
| DELETE | `/carrinho/{id}` | Remove item |

**Exemplo POST /carrinho:**
```json
{
  "id": 101,
  "titulo": "Morango Orgânico",
  "preco": 5.90,
  "imagem": "https://...",
  "quantidade": 2
}
```

---

### 📦 Produtos

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/produtos` | Lista todos os produtos |
| POST | `/produtos` | Adiciona novo produto |
| POST | `/seed-produtos` | Popula banco com catálogo inicial |

**Exemplo GET /produtos:**
```json
[
  {
    "id": 101,
    "titulo": "Morango Fresco Orgânico",
    "preco": 5.90,
    "categoria": "frutas",
    "imagem": "https://...",
    "imagens_adicionais": "url1,url2,url3"
  }
]
```

---

### 📍 Geolocalização

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/geolocalizacao/busca` | Busca lojas por CEP |
| POST | `/geolocalizacao/rota` | Calcula rota entre dois pontos |
| GET | `/geolocalizacao/favoritos` | Lista lojas favoritas |
| POST | `/geolocalizacao/favoritos` | Adiciona favorito |
| PUT | `/geolocalizacao/favoritos/{id}` | Atualiza apelido |
| DELETE | `/geolocalizacao/favoritos/{id}` | Remove favorito |

**Exemplo POST /geolocalizacao/busca:**

```json
{
  "cep_usuario": "03650010"
}
```

**Resposta:**
```json
{
  "cep_origem": "03650010",
  "lat_usuario": -23.5355,
  "lon_usuario": -46.5195,
  "lojas": [
    {
      "id": 1,
      "nome": "Natural Fresh - Vila Matilde",
      "cidade": "São Paulo",
      "bairro": "Vila Matilde",
      "distancia": 0.85,
      "lat": -23.53,
      "lon": -46.52,
      "fotos": ["url1", "url2"]
    }
  ]
}
```

---

## 🗄️ Banco de Dados

### Schema PostgreSQL

```sql
-- Tabela de Produtos
CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR NOT NULL,
    preco FLOAT NOT NULL,
    categoria VARCHAR NOT NULL,
    imagem VARCHAR NOT NULL,
    imagens_adicionais VARCHAR
);

-- Tabela de Unidades Físicas
CREATE TABLE unidades_fisicas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR NOT NULL,
    cidade VARCHAR NOT NULL,
    bairro VARCHAR NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    descricao VARCHAR,
    fotos VARCHAR
);

-- Tabela de Favoritos
CREATE TABLE favoritos (
    id SERIAL PRIMARY KEY,
    loja_id INTEGER REFERENCES unidades_fisicas(id),
    apelido VARCHAR NOT NULL,
    cep_usuario VARCHAR NOT NULL
);

-- Tabela de Carrinho
CREATE TABLE carrinho (
    id BIGINT PRIMARY KEY,
    titulo VARCHAR NOT NULL,
    preco FLOAT NOT NULL,
    quantidade INTEGER NOT NULL,
    imagem VARCHAR NOT NULL
);
```

---

## 🔌 Integrações Externas

### 1. ViaCEP
- **Documentação**: https://viacep.com.br/
- **Uso**: Buscar endereço completo por CEP
- **Gratuito**: Sim
- **Licença**: Sem restrições

**Exemplo:**
```python
GET https://viacep.com.br/ws/03650010/json/
```

### 2. Geoapify
- **Documentação**: https://www.geoapify.com/
- **Uso**: Geocoding e cálculo de rotas
- **Gratuito**: Até 3.000 requisições/dia
- **Licença**: Necessário cadastro

**Cadastro:**
1. Acesse https://www.geoapify.com/
2. Crie conta gratuita
3. Copie API Key do dashboard
4. Adicione em `.env`:
```env
GEOAPIFY_API_KEY=sua_chave_aqui
```

---

## ⚙️ Configuração

### Variáveis de Ambiente (.env)

```env
# Banco de Dados
DATABASE_URL=postgresql+psycopg2://usuario:senha@localhost:5432/natural_organic_db

# API Externa
GEOAPIFY_API_KEY=sua_chave_geoapify
```

---

## 🐳 Docker

### Dockerfile Completo

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose (com banco de dados)

```yaml
services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: mvp_puc_2026
      POSTGRES_DB: natural_organic_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin"]
      interval: 5s
      timeout: 5s
      retries: 5

  api:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
    environment:
      DATABASE_URL: postgresql+psycopg2://admin:mvp_puc_2026@db:5432/natural_organic_db
    env_file:
      - .env

volumes:
  postgres_data:
```

**Executar:**
```bash
docker-compose up --build
```

---

## 📸 Swagger

![Swagger](docs/swagger.png)

---

## 📊 Diagrama de Arquitetura

  ![Diagrama de Arquitetura](docs/image.png)
