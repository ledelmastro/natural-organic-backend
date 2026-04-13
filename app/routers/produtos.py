from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import ProdutoDB
from ..schemas import ProdutoCreate

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.get("/")
def listar(db: Session = Depends(get_db)):
    return db.query(ProdutoDB).all()

@router.post("/")
def criar(produto: ProdutoCreate, db: Session = Depends(get_db)):
    data = produto.model_dump()

    if data.get("imagens_adicionais"):
        data["imagens_adicionais"] = ",".join(data["imagens_adicionais"])

    novo = ProdutoDB(**data)
    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo

@router.post("/seed", include_in_schema=False)
def seed_produtos(db: Session = Depends(get_db)):
    catalogo = [
  {
    "id": 101,
    "titulo": "Morango Fresco Orgânico",
    "preco": 5.90,
    "categoria": "frutas",
    "imagem": "https://images.pexels.com/photos/34191839/pexels-photo-34191839.jpeg?auto=format&fit=crop&q=80&w=800",
    "imagens_adicionais": [
        "https://images.pexels.com/photos/33415840/pexels-photo-33415840.jpeg?auto=format&fit=crop&q=80&w=400",
        "https://images.pexels.com/photos/8670502/pexels-photo-8670502.jpeg?auto=format&fit=crop&q=80&w=400"
    ]
  },
  {
    "id": 102,
    "titulo": "Abacate Maduro",
    "preco": 12.50,
    "categoria": "vegetais",
    "imagem": "https://images.pexels.com/photos/35155933/pexels-photo-35155933.jpeg?auto=format&fit=crop&q=80&w=800",
    "imagens_adicionais": [
        "https://images.pexels.com/photos/3872372/pexels-photo-3872372.jpeg?auto=format&fit=crop&q=80&w=400",
        "https://images.pexels.com/photos/19610913/pexels-photo-19610913.jpeg?auto=format&fit=crop&q=80&w=400"
    ]
  },
  {
    "id": 103,
    "titulo": "Laranja Orgânica",
    "preco": 3.20,
    "categoria": "frutas",
    "imagem": "https://images.unsplash.com/photo-1582979512210-99b6a53386f9?auto=format&fit=crop&q=80&w=800",
    "imagens_adicionais": [
        "https://images.unsplash.com/photo-1611080626919-7cf5a9dbab5b?auto=format&fit=crop&q=80&w=400",
        "https://images.unsplash.com/photo-1557800636-894a64c1696f?auto=format&fit=crop&q=80&w=400"
    ]
  },
  {
    "id": 104,
    "titulo": "Manga Fresca Exótica",
    "preco": 8.90,
    "categoria": "frutas",
    "imagem": "https://images.unsplash.com/photo-1553279768-865429fa0078?auto=format&fit=crop&q=80&w=800",
    "imagens_adicionais": [
        "https://images.unsplash.com/photo-1601493700631-2b16ec4b4716?auto=format&fit=crop&q=80&w=400",
        "https://images.unsplash.com/photo-1591073113125-e46713c829ed?auto=format&fit=crop&q=80&w=400"
    ]
  },
  {
    "id": 105,
    "titulo": "Maçã Vermelha Crocante",
    "preco": 2.50,
    "categoria": "frutas",
    "imagem": "https://images.pexels.com/photos/9303984/pexels-photo-9303984.jpeg?auto=format&fit=crop&q=80&w=800",
    "imagens_adicionais": [
        "https://images.pexels.com/photos/33591389/pexels-photo-33591389.jpeg?auto=format&fit=crop&q=80&w=400",
        "https://images.pexels.com/photos/10520131/pexels-photo-10520131.jpeg?auto=format&fit=crop&q=80&w=400"
    ]
  },
  {
    "id": 106,
    "titulo": "Pacote de Mirtilos Orgânicos",
    "preco": 22.00,
    "categoria": "frutas",
    "imagem": "https://images.unsplash.com/photo-1498557850523-fd3d118b962e?auto=format&fit=crop&q=80&w=800",
    "imagens_adicionais": [
        "https://images.unsplash.com/photo-1592394533824-9440e5d68530?auto=format&fit=crop&q=80&w=400",
        "https://images.unsplash.com/photo-1425934398893-310a009a77f9?auto=format&fit=crop&q=80&w=400"
    ]
  },
  {
    "id": 107,
    "titulo": "Brócolis Fresco",
    "preco": 4.00,
    "categoria": "vegetais",
    "imagem": "https://images.pexels.com/photos/9348461/pexels-photo-9348461.jpeg?auto=format&fit=crop&q=80&w=800",
    "imagens_adicionais": [
        "https://images.pexels.com/photos/30931704/pexels-photo-30931704.jpeg?auto=format&fit=crop&q=80&w=400",
        "https://images.pexels.com/photos/7454754/pexels-photo-7454754.jpeg?auto=format&fit=crop&q=80&w=400"
    ]
  },
  {
    "id": 108,
    "titulo": "Suco de Cenoura Prensado",
    "preco": 6.50,
    "categoria": "sucos",
    "imagem": "https://images.pexels.com/photos/32751756/pexels-photo-32751756.jpeg?auto=format&fit=crop&q=80&w=800",
    "imagens_adicionais": [
        "https://images.pexels.com/photos/7500451/pexels-photo-7500451.jpeg?auto=format&fit=crop&q=80&w=400",
        "https://images.pexels.com/photos/5946662/pexels-photo-5946662.jpeg?auto=format&fit=crop&q=80&w=400"
    ]
  },
  {
    "id": 109,
    "titulo": "Cenoura Baby Selecionada",
    "preco": 8.90,
    "categoria": "legumes",
    "imagem": "https://images.pexels.com/photos/143133/pexels-photo-143133.jpeg?auto=format&fit=crop&q=80&w=800",
    "imagens_adicionais": [
      "https://images.pexels.com/photos/65174/pexels-photo-65174.jpeg?auto=format&fit=crop&q=80&w=400",
      "https://images.pexels.com/photos/1306559/pexels-photo-1306559.jpeg?auto=format&fit=crop&q=80&w=400"
    ]
  },
  {
    "id": 110,
    "titulo": "Cebola Roxa Orgânica",
    "preco": 5.40,
    "categoria": "legumes",
    "imagem": "https://images.unsplash.com/photo-1668295037469-8b0e8d11cd2a?q=80&w=1171&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D?auto=format&fit=crop&q=80&w=800",
    "imagens_adicionais": [
      "https://images.unsplash.com/photo-1664975367126-e3f1c9b44e07?q=80&w=765&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D?auto=format&fit=crop&q=80&w=400",
      "https://plus.unsplash.com/premium_photo-1700400119867-41aeda606042?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D?auto=format&fit=crop&q=80&w=400"
    ]
  },
  {
    "id": 111,
    "titulo": "Couve Manteiga Fresca",
    "preco": 4.20,
    "categoria": "verduras",
    "imagem": "https://images.unsplash.com/photo-1448030081970-b7d1ae923ed6?q=80&w=1074&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D?auto=format&fit=crop&q=80&w=800",
    "imagens_adicionais": [
      "https://images.unsplash.com/photo-1486328228599-85db4443971f?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D?auto=format&fit=crop&q=80&w=400",
      "https://plus.unsplash.com/premium_photo-1707242994962-e3fd3ecd7b26?q=80&w=735&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D?auto=format&fit=crop&q=80&w=400"
    ]
  },
  {
    "id": 112,
    "titulo": "Espinafre em Folhas Maço",
    "preco": 4.80,
    "categoria": "verduras",
    "imagem": "https://plus.unsplash.com/premium_photo-1703260007808-bdc648fd29b7?q=80&w=688&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D?auto=format&fit=crop&q=80&w=800",
    "imagens_adicionais": [
      "https://images.unsplash.com/photo-1583681781586-b980500f327a?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D?auto=format&fit=crop&q=80&w=400",
      "https://images.unsplash.com/photo-1580910365246-e897eca689b1?q=80&w=1152&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D?auto=format&fit=crop&q=80&w=400"
    ]
  },
  {
    "id": 113,
    "titulo": "Pimentão Amarelo Premium",
    "preco": 7.30,
    "categoria": "legumes",
    "imagem": "https://images.unsplash.com/photo-1741515042519-9b52d3ec2eaf?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D?auto=format&fit=crop&q=80&w=800",
    "imagens_adicionais": [
      "https://images.unsplash.com/photo-1741515042633-fabad7ce2c57?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D?auto=format&fit=crop&q=80&w=400",
      "https://images.unsplash.com/photo-1693618712552-a4d5cb0cf6c2?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D?auto=format&fit=crop&q=80&w=400"
    ]
  },
  {
    "id": 114,
    "titulo": "Grão-de-Bico Cozido a Vapor",
    "preco": 12.50,
    "categoria": "graos",
    "imagem": "https://plus.unsplash.com/premium_photo-1666649675085-406bc5cea8e0?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D?auto=format&fit=crop&q=80&w=800",
    "imagens_adicionais": [
      "https://images.unsplash.com/photo-1708521203088-eb479776e1a9?q=80&w=1074&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D?auto=format&fit=crop&q=80&w=400",
      "https://images.unsplash.com/photo-1761095596792-2735f03c7418?q=80&w=1171&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D?auto=format&fit=crop&q=80&w=400"
    ]
  },
  {
    "id": 115,
    "titulo": "Lentilha Vermelha Seca",
    "preco": 10.90,
    "categoria": "graos",
    "imagem": "https://images.unsplash.com/photo-1730591857303-0fa44be3f677?q=80&w=993&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D?auto=format&fit=crop&q=80&w=800",
    "imagens_adicionais": [
      "https://plus.unsplash.com/premium_photo-1701064865216-4306843a809f?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D?auto=format&fit=crop&q=80&w=400",
      "https://images.unsplash.com/photo-1764573464925-da17a9f796d4?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D?auto=format&fit=crop&q=80&w=400"
    ]
  },
  {
    "id": 116,
    "titulo": "Ervilha Tortinha Fresca",
    "preco": 9.20,
    "categoria": "graos",
    "imagem": "https://images.unsplash.com/photo-1560705185-d0291220a442?q=80&w=1074&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D?auto=format&fit=crop&q=80&w=800",
    "imagens_adicionais": [
      "https://images.unsplash.com/photo-1697813586273-bd0ada83c395?q=80&w=735&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D?auto=format&fit=crop&q=80&w=400",
      "https://plus.unsplash.com/premium_photo-1663844169552-abecefbfa045?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D?auto=format&fit=crop&q=80&w=400"
    ]
  },
  {
    "id": 117,
    "titulo": "Mix de Grãos Ancestrais",
    "preco": 15.60,
    "categoria": "graos",
    "imagem": "https://images.unsplash.com/photo-1615485290628-c5033c657a8c?q=80&w=880&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D?auto=format&fit=crop&q=80&w=800",
    "imagens_adicionais": [
      "https://images.unsplash.com/photo-1698845650846-4119019ddf05?q=80&w=1176&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D?auto=format&fit=crop&q=80&w=400",
      "https://plus.unsplash.com/premium_photo-1664007710992-ad36b7943edb?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D?auto=format&fit=crop&q=80&w=400"
    ]
  },
  {
    "id": 118,
    "titulo": "Pimentão Vermelho Premium",
    "preco": 7.50,
    "categoria": "legumes",
    "imagem": "https://images.unsplash.com/photo-1737099901224-b0282880e6d8?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D?q=80&w=880&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D?auto=format&fit=crop&q=80&w=800",
    "imagens_adicionais": [
      "https://images.unsplash.com/photo-1760361571885-b6b2dee1d25a?q=80&w=1210&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D?auto=format&fit=crop&q=80&w=400",
      "https://images.unsplash.com/photo-1594443602313-7261e6dc2c0d?q=80&w=735&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D?auto=format&fit=crop&q=80&w=400"
    ]
  }
    ]

    for item in catalogo:
        existe = db.query(ProdutoDB).filter(ProdutoDB.id == item["id"]).first()
        if not existe:
            novo_p = ProdutoDB(
                id=item["id"],
                titulo=item["titulo"],
                preco=item["preco"],
                categoria=item["categoria"],
                imagem=item["imagem"],
                imagens_adicionais=",".join(item["imagens_adicionais"]) if item.get("imagens_adicionais") else None
            )
            db.add(novo_p)
    db.commit()
    return {"status": "Produtos populados com sucesso!"}