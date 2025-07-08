
from pydantic import BaseModel
from datetime import date

class CartaoDeCreditoRequest(BaseModel):
    numero_cartao: str
    nome_titular: str
    validade: date
    cvv: str
