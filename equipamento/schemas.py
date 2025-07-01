from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)


class BicicletaUpdate(BaseModel):
    numero: int
    marca: Optional[str]
    modelo: Optional[str]
    ano: Optional[str]
    
    model_config = ConfigDict(from_attributes=True)


# Totem
class TotemRequest(BaseModel):
    localizacao: str
    descricao: str


class TotemResponse(BaseModel):
    numero: int
    localizacao: str
    descricao: str

    model_config = ConfigDict(from_attributes=True)


class TotemUpdate(BaseModel):
    numero: int
    localizacao: Optional[str]
    descricao: Optional[str]
    
    model_config = ConfigDict(from_attributes=True)
