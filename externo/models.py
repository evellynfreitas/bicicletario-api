from database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

class Cobranca(Base):
    __tablename__ = "cobranca"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    status = Column(String)
    hora_solicitacao = Column(DateTime, default=datetime.today())
    hora_finalizacao = Column(DateTime, nullable=True)
    ciclista = Column(Integer, nullable=False)
    valor = Column(Float)