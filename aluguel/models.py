from database import Base
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime

class Ciclista(Base):
    __tablename__ = "ciclistas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String)
    email = Column(String, unique=True, index=True)
    nacionalidade = Column(String)
    cpf = Column(String, nullable=True)
    passaporte = Column(String, nullable=True)
    senha = Column(String)
    data_nascimento = Column(Date)
    ativo = Column(Boolean, default=False)
    data_hora_confirmacao = Column(DateTime, nullable=True)
    cartao = relationship("CartaoDeCredito", back_populates="ciclista", uselist=False)

class CartaoDeCredito(Base):
    __tablename__ = "cartao_de_credito"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_ciclista = Column(Integer, ForeignKey("ciclistas.id"), nullable=False, unique=True)

    numero_cartao = Column(String)
    nome_titular = Column(String)
    validade = Column(Date)
    cvv = Column(String)

    ciclista = relationship("Ciclista", back_populates="cartao")

class Funcionario(Base):
    __tablename__ = "funcionarios"

    matricula = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String)
    email = Column(String, unique=True, index=True)
    cpf = Column(String)
    funcao = Column(String)
    senha = Column(String)
    data_nascimento = Column(Date)

class Aluguel(Base):
    __tablename__ = "aluguel"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_ciclista = Column(Integer, ForeignKey("ciclistas.id"), nullable=False)
    id_bicicleta = Column(Integer, nullable=False)
    tranca_inicial = Column(Integer, nullable=False)
    hora_inicio = Column(DateTime, default=datetime.today())
    hora_fim = Column(DateTime, default=datetime.today())
    cobranca = Column(Float)
    
    ciclista = relationship("Ciclista")
    