from pydantic import BaseModel, Field
from typing import Tuple, Optional, List

class ItemCarrinho(BaseModel):
    id: int
    titulo: str
    preco: float
    quantidade: int
    imagem: str

class ProdutoCreate(BaseModel):
    titulo: str
    preco: float
    categoria: str
    imagem: str
    imagens_adicionais: Optional[List[str]] = []
    
    class Config:
        from_attributes = True

# 🔹 GELOCALIZAÇÃO - ROTA
class RotaRequest(BaseModel):
    origem: Tuple[float, float] = Field(..., description="Latitude e longitude de origem")
    destino: Tuple[float, float] = Field(..., description="Latitude e longitude de destino")

# 🔹 BUSCA DE CEP
class BuscaCEPRequest(BaseModel):
    loja_id: Optional[int] = 0
    apelido: Optional[str] = "busca"
    cep_usuario: str = Field(..., min_length=8, max_length=8)

# 🔹 FAVORITOS
class FavoritoRequest(BaseModel):
    loja_id: int
    apelido: str
    cep_usuario: str

class CoordenadasRequest(BaseModel):
    lat: float
    lon: float