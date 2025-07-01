from pydantic import BaseModel
from datetime import date
from typing import Optional


# Bicicleta
class BicicletaRequest(BaseModel):
    marca: str
    modelo: str
    ano: str


class BicicletaResponse(BaseModel):
    numero: int
    marca: str
    modelo: str
    ano: str
    status: str
    localizacao: str

    class Config:
        from_attributes = True


class BicicletaUpdate(BaseModel):
    numero: int
    marca: Optional[str]
    modelo: Optional[str]
    ano: Optional[str]
    
    class Config:
        from_attributes = True

