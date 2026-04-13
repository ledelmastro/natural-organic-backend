from sqlalchemy import Column, Integer, String, Float, ForeignKey, BigInteger
from .database import Base

class UnidadeFisicaDB(Base):
    __tablename__ = "unidades_fisicas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    cidade = Column(String)
    bairro = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    descricao = Column(String, nullable=True)
    fotos = Column(String, nullable=True)  # Salvaremos como string separada por vírgulas

class FavoritoDB(Base):
    __tablename__ = "favoritos"
    id = Column(Integer, primary_key=True, index=True)
    loja_id = Column(Integer, ForeignKey("unidades_fisicas.id"))
    apelido = Column(String)
    cep_usuario = Column(String)

class CarrinhoDB(Base):
    __tablename__ = "carrinho"
    # id vindo do produto, por isso autoincrement=False
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=False)
    titulo = Column(String)
    preco = Column(Float)
    quantidade = Column(Integer)
    imagem = Column(String)

class ProdutoDB(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    preco = Column(Float)
    categoria = Column(String)
    imagem = Column(String)
    imagens_adicionais = Column(String, nullable=True)