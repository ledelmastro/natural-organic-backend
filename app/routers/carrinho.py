from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import CarrinhoDB
from ..schemas import ItemCarrinho

router = APIRouter(prefix="/carrinho", tags=["Carrinho"])

@router.get("/")
def listar_carrinho(db: Session = Depends(get_db)):
    return db.query(CarrinhoDB).order_by(CarrinhoDB.id).all()

@router.post("/")
def adicionar_ao_carrinho(item: ItemCarrinho, db: Session = Depends(get_db)):
    db_item = db.query(CarrinhoDB).filter(CarrinhoDB.id == item.id).first()
    if db_item:
        db_item.quantidade += item.quantidade
    else:
        db.add(CarrinhoDB(**item.model_dump()))
    db.commit()
    return {"status": "sucesso", "item": item}

@router.put("/{id_item}")
def atualizar_item_carrinho(id_item: int, quantidade: int, db: Session = Depends(get_db)):
    db_item = db.query(CarrinhoDB).filter(CarrinhoDB.id == id_item).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    db_item.quantidade = quantidade
    db.commit()
    return {"mensagem": "Atualizado", "item": db_item.titulo}

@router.delete("/{id_item}")
def remover_item_carrinho(id_item: int, db: Session = Depends(get_db)):
    db_item = db.query(CarrinhoDB).filter(CarrinhoDB.id == id_item).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item não existe")
    db.delete(db_item)
    db.commit()
    return {"mensagem": "Removido"}