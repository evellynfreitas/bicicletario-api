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


# Tranca
class TrancaRequest(BaseModel):
    modelo: str
    ano_fabricacao: str
    localizacao: str


class TrancaResponse(BaseModel):
    numero: int
    modelo: str
    ano_fabricacao: str
    status: str
    localizacao: str

    model_config = ConfigDict(from_attributes=True)


class TrancaUpdate(BaseModel):
    numero: int
    modelo: Optional[str]
    ano_fabricacao: Optional[str]
    localizacao: Optional[str]
    
    model_config = ConfigDict(from_attributes=True)

