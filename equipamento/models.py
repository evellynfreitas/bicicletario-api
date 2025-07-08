from database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

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

    bicicleta_numero = Column(Integer, ForeignKey("bicicletas.numero"), nullable=True)
    bicicleta = relationship("Bicicleta", backref="trancas")

class Reparo(Base):
    __tablename__ = "reparos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    bicicleta_numero = Column(Integer, ForeignKey("bicicletas.numero"))
    funcionario_id = Column(Integer)
    data_retirada = Column(DateTime, default=datetime.now())
    data_retorno = Column(DateTime, nullable=True)

    bicicleta = relationship("Bicicleta")

