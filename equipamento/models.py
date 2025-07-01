from database import Base
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

class Bicicleta(Base):
    __tablename__ = "bicicletas"

    numero = Column(Integer, primary_key=True, index=True, autoincrement=True)
    marca = Column(String)
    modelo = Column(String)
    ano = Column(String)
    status = Column(String, default="NOVA")
    localizacao = Column(String, nullable=True)
    
