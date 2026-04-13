import os
import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from geopy.distance import geodesic
from ..database import get_db
from ..models import UnidadeFisicaDB, FavoritoDB
from ..schemas import BuscaCEPRequest, FavoritoRequest, RotaRequest, CoordenadasRequest

router = APIRouter(prefix="/geolocalizacao", tags=["Geolocalização"])

# Função para converter CEP em Lat/Log
def obter_coords_por_cep(cep):
    cep_limpo = "".join(filter(str.isdigit, str(cep)))
    print("📦 CEP recebido:", cep_limpo)

    try:
        # 🔹 1. ViaCEP (descobre endereço real)
        viacep_url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
        resp = requests.get(viacep_url, timeout=5)

        if resp.status_code != 200:
            print("❌ Erro ViaCEP")
            return None

        data = resp.json()

        if "erro" in data:
            print("❌ CEP inválido")
            return None

        endereco = f"{data['logradouro']}, {data['bairro']}, {data['localidade']}, Brazil"
        print("📍 Endereço:", endereco)

        # 🔹 2. Geoapify (transforma em coordenadas)
        API_KEY = os.getenv("GEOAPIFY_API_KEY")

        if not API_KEY:
            raise ValueError("API KEY não encontrada. Configure no .env")

        geo_url = (
            f"https://api.geoapify.com/v1/geocode/search?"
            f"text={endereco}&format=json&apiKey={API_KEY}"
        )

        geo_resp = requests.get(geo_url, timeout=5)

        if geo_resp.status_code == 200:
            geo_data = geo_resp.json()

            if geo_data.get("results"):
                lat = geo_data["results"][0]["lat"]
                lon = geo_data["results"][0]["lon"]

                print("✅ Coordenadas:", lat, lon)
                return float(lat), float(lon)

        print("⚠️ Geoapify não retornou resultado")

    except Exception as e:
        print("⚠️ Erro ao buscar CEP:", e)

    return None

@router.post("/rota")
def gerar_rota(data: RotaRequest):
    origem = data.origem
    destino = data.destino
    
    API_KEY = os.getenv("GEOAPIFY_API_KEY")

    if not API_KEY:
        raise ValueError("API KEY não encontrada. Verifique as variáveis de ambiente.")
    url = "https://api.geoapify.com/v1/routing"

    waypoints = f"{origem[0]},{origem[1]}|{destino[0]},{destino[1]}"
    
    print(f"DEBUG WAYPOINTS: {waypoints}") # Verifique no terminal do Python se aparece algo como -23.5,-46.6|-23.5,-46.5

    params = {
        "waypoints": waypoints,
        "mode": "drive",
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Erro Geoapify: {response.status_code} - {response.text}")
        raise HTTPException(status_code=400, detail="Erro ao gerar rota na API externa")

    rota_data = response.json()
    if not rota_data.get("features"):
        raise HTTPException(status_code=400, detail="Nenhuma rota encontrada")

    return rota_data

@router.post("/busca")
def encontrar_lojas_proximas(request: BuscaCEPRequest, db: Session = Depends(get_db)):
    # 1. Obtém as coordenadas do CEP digitado
    user_coords = obter_coords_por_cep(request.cep_usuario)
    
    # Se falhar, usa a Praça da Sé (São Paulo) como padrão
    if not user_coords:
        print(f"⚠️ CEP {request.cep_usuario} não localizado. Usando padrão Sé.")
        user_coords = (-23.5505, -46.6333)

    # 2. Busca todas as lojas no banco
    todas_lojas = db.query(UnidadeFisicaDB).all()
    lista_proximidade = []
    
    # 3. Calcula a distância de cada loja para o usuário
    for loja in todas_lojas:
        if loja.latitude and loja.longitude:
            dist = geodesic(user_coords, (loja.latitude, loja.longitude)).km
            lista_proximidade.append({
                "id": loja.id,
                "nome": loja.nome,
                "cidade": loja.cidade,
                "bairro": loja.bairro,
                "distancia": round(dist, 2),
                "lat": loja.latitude,
                "lon": loja.longitude,
                "descricao": loja.descricao or "Venha conhecer nossa seleção de produtos naturais.",
                "fotos": (loja.fotos or "").split(",")
            })

    # 4. Ordena pelas mais próximas e pega as 4 primeiras
    lojas_ordenadas = sorted(lista_proximidade, key=lambda x: x['distancia'])[:4]
    
    # 5. Retorna os dados para o Frontend (incluindo a posição do usuário para o mapa)
    return {
        "cep_origem": request.cep_usuario,
        "lat_usuario": user_coords[0],
        "lon_usuario": user_coords[1],
        "lojas": lojas_ordenadas
    }

@router.post("/coords")
def buscar_por_coordenadas(data: CoordenadasRequest, db: Session = Depends(get_db)):
    lat = data.lat
    lon = data.lon
    user_coords = (lat, lon)
    
    todas_lojas = db.query(UnidadeFisicaDB).all()
    lista_proximidade = []
    
    for loja in todas_lojas:
        if loja.latitude and loja.longitude:
            dist = geodesic(user_coords, (loja.latitude, loja.longitude)).km
            lista_proximidade.append({
                "id": loja.id,
                "nome": loja.nome,
                "cidade": loja.cidade,
                "bairro": loja.bairro,
                "distancia": round(dist, 2),
                "lat": loja.latitude,
                "lon": loja.longitude,
                "descricao": loja.descricao or "Venha conhecer nossa seleção de produtos naturais.",
                "fotos": (loja.fotos or "https://images.unsplash.com/photo-1542838132-92c53300491e").split(",")
            })

    lojas_ordenadas = sorted(lista_proximidade, key=lambda x: x['distancia'])[:4]
    return {"lojas": lojas_ordenadas}

@router.get("/favoritos")
def listar_favoritos(db: Session = Depends(get_db)):
    # Fazemos um Join para trazer os dados da UnidadeFisica junto com o favorito
    favoritos = db.query(FavoritoDB, UnidadeFisicaDB).join(
        UnidadeFisicaDB, FavoritoDB.loja_id == UnidadeFisicaDB.id
    ).all()
    
    resultado = []
    for fav, loja in favoritos:
        resultado.append({
            "id_favorito": fav.id,
            "loja_id": loja.id,
            "apelido": fav.apelido,
            "cep_usuario": fav.cep_usuario,
            "nome_loja": loja.nome,
            "bairro": loja.bairro,
            "cidade": loja.cidade
        })
    return resultado

@router.put("/favoritos/{id_favorito}")
def atualizar_favorito(id_favorito: int, request: FavoritoRequest, db: Session = Depends(get_db)):
    fav = db.query(FavoritoDB).filter(FavoritoDB.id == id_favorito).first()
    if not fav:
        raise HTTPException(status_code=404, detail="Favorito não encontrado")
    
    fav.apelido = request.apelido
    fav.cep_usuario = request.cep_usuario
    db.commit()
    return {"mensagem": "Favorito atualizado com sucesso"}

@router.post("/favoritos")
def salvar_favorito(request: FavoritoRequest, db: Session = Depends(get_db)):
    novo_fav = FavoritoDB(**request.model_dump())
    db.add(novo_fav)
    db.commit()
    return {"mensagem": "Salvo"}

@router.delete("/favoritos/{id_favorito}")
def deletar_favorito(id_favorito: int, db: Session = Depends(get_db)):
    fav = db.query(FavoritoDB).filter(FavoritoDB.id == id_favorito).first()
    if not fav:
        raise HTTPException(status_code=404, detail="Favorito não encontrado")
    db.delete(fav)
    db.commit()
    return {"mensagem": "Local favorito removido"}