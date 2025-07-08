from database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime

class Cobranca(Base):
    __tablename__ = "cobranca"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    status = Column(String)
    hora_solicitacao = Column(DateTime)
    hora_finalizacao = Column(DateTime)
    ciclista = Column(Integer, nullable=False)
    valor = Column(Float)