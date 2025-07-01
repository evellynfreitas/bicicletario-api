from database import Base
from sqlalchemy import Column, Integer, String

class Bicicleta(Base):
    __tablename__ = "bicicletas"

    numero = Column(Integer, primary_key=True, index=True, autoincrement=True)
    marca = Column(String)
    modelo = Column(String)
    ano = Column(String)
    status = Column(String, default="NOVA")
    localizacao = Column(String, nullable=True)

class Totem(Base):
    __tablename__ = "totens"

    numero = Column(Integer, primary_key=True, index=True, autoincrement=True)
    localizacao = Column(String)
    descricao = Column(String)

class Tranca(Base):
    __tablename__ = "trancas"

    numero = Column(Integer, primary_key=True, index=True, autoincrement=True)
    localizacao = Column(String)
    ano_fabricacao = Column(String)
    modelo = Column(String)
    status = Column(String, default="NOVA")
