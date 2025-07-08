
from pydantic import BaseModel
from datetime import date, datetime

class CartaoDeCreditoRequest(BaseModel):
    numero_cartao: str
    nome_titular: str
    validade: date
    cvv: str

class CobrancaRequest(BaseModel):
    valor: float
    ciclista: int


class CobrancaResponse(BaseModel):
    valor: float
    ciclista: int
    status: str
    id: int
    hora_solicitacao: datetime
    hora_finalizacao: datetime
    
    