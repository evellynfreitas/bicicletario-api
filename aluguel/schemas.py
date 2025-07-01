from pydantic import BaseModel
from datetime import date
from typing import Optional


# Cartão de Crédito

class CartaoDeCreditoRequest(BaseModel):
    numero_cartao: str
    nome_titular: str
    validade: date
    cvv: str

class CartaoDeCreditoResponse(BaseModel):
    id: int
    nome: str
    email: str
    nacionalidade: str
    data_nascimento: date
    ativo: bool

    class Config:
        from_attributes = True

# Ciclista
class CiclistaRequest(BaseModel):
    nome: str
    email: str
    cpf: Optional[str] = None
    passaporte: Optional[str] = None
    nacionalidade: str
    senha: str
    data_nascimento: date
    cartao_de_credito: CartaoDeCreditoRequest

class CiclistaResponse(BaseModel):
    id: int
    nome: str
    email: str
    nacionalidade: str
    data_nascimento: date
    ativo: bool

    class Config:
        from_attributes = True


class CiclistaUpdate(BaseModel):
    nome: Optional[str]
    email: Optional[str]
    senha: Optional[str]
    data_nascimento: Optional[date]

    class Config:
        from_attributes = True


# Funcionario

class FuncionarioRequest(BaseModel):
    nome: str
    email: str
    cpf: str
    funcao: str
    senha: str
    data_nascimento: date

class FuncionarioResponse(BaseModel):
    matricula: int
    nome: str
    email: str
    cpf: str
    funcao: str
    data_nascimento: date

    class Config:
        from_attributes = True

class FuncionarioUpdate(BaseModel):
    matricula: int
    nome: Optional[str]
    email: Optional[str]
    senha: Optional[str]
    funcao: Optional[str]
    cpf: Optional[str]
    data_nascimento: Optional[date]

    class Config:
        from_attributes = True
