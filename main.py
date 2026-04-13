import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, SessionLocal, Base
from app.models import UnidadeFisicaDB, ProdutoDB
from app.routers import carrinho, produtos, geolocalizacao

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Garante a criação das tabelas no startup
    Base.metadata.create_all(bind=engine)
    
    # Seed de Unidades Físicas
    db = SessionLocal()
    try:
        if db.query(UnidadeFisicaDB).count() == 0:
            print("🌱 Populando banco de dados com unidades iniciais...")
            lojas_iniciais = [
                {
                    "nome": "Natural Fresh - Vila Matilde", 
                    "cidade": "São Paulo", "bairro": "Vila Matilde", 
                    "latitude": -23.53, "longitude": -46.52,
                    "descricao": "Nossa unidade mais aconchegante, focada em produtos colhidos no dia.",
                    "fotos": "https://images.unsplash.com/photo-1542838132-92c53300491e,https://images.unsplash.com/photo-1578916171728-46686eac8d58"
                },
                {
                    "nome": "Natural Fresh - Centro", 
                    "cidade": "São Paulo", "bairro": "Sé", 
                    "latitude": -23.55, "longitude": -46.63,
                    "descricao": "Localizada no coração da cidade, com a maior variedade de produtos orgânicos importados.",
                    "fotos": "https://images.unsplash.com/photo-1534723452862-4c874018d66d,https://images.unsplash.com/photo-1604719312566-8912e9227c6a"
                },
                {
                    "nome": "Natural Fresh - Campinas", 
                    "cidade": "Campinas", "bairro": "Cambuí", 
                    "latitude": -22.89, "longitude": -47.04,
                    "descricao": "Espaço amplo com cafeteria orgânica e workshops de culinária saudável.",
                    "fotos": "https://images.unsplash.com/photo-1583258292688-d0213dc5a3a8,https://images.unsplash.com/photo-1506617420156-8e4536971650"
                }
            ]
            for loja in lojas_iniciais:
                db.add(UnidadeFisicaDB(**loja))
            db.commit()

        # Seed automático de produtos se estiver vazio
        if db.query(ProdutoDB).count() == 0:
            from app.routers.produtos import seed_produtos
            seed_produtos(db)
            
    except Exception as e:
        print(f"⚠️ Erro ao popular banco no startup: {e}")
    finally:
        db.close()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluindo as rotas modulares
app.include_router(carrinho.router)
app.include_router(produtos.router)
app.include_router(geolocalizacao.router)