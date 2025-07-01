from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Ciclista, CartaoDeCredito
from schemas import CiclistaRequest, CiclistaResponse, CiclistaUpdate
from datetime import datetime
import re

def verifica_email_cadastrado(email: str, db: Session) -> bool:
    return db.query(Ciclista).filter(Ciclista.email == email).first() is not None

def email_valido(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def valida_documento(nacionalidade: str, cpf: str, passaporte: str) -> bool:
    if nacionalidade.upper() in ['BRASILEIRA', 'BRASILEIRO']:
        return cpf is not None
    return passaporte is not None

def valida_cartao(cartao) -> bool:
    # Placeholder — lógica de validação real pode ser adicionada aqui
    return True

def envia_email_cadastro(email: str):
    print(f"Enviei o email de confirmação para {email}.")

def cria_ciclista(request: CiclistaRequest, db: Session) -> Ciclista:
    if verifica_email_cadastrado(request.email, db):
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    if not email_valido(request.email):
        raise HTTPException(status_code=400, detail="Email não é válido")

    if not valida_documento(request.nacionalidade, request.cpf, request.passaporte):
        raise HTTPException(status_code=400, detail="Documentos não preenchidos corretamente")

    if not valida_cartao(request.cartao_de_credito):
        raise HTTPException(status_code=400, detail="Cartão de crédito inválido")

    novo_ciclista = Ciclista(
        nome=request.nome,
        email=request.email,
        nacionalidade=request.nacionalidade,
        senha=request.senha,
        cpf=request.cpf,
        passaporte=request.passaporte,
        data_nascimento=request.data_nascimento
    )
    db.add(novo_ciclista)
    db.commit()
    db.refresh(novo_ciclista)

    novo_cartao = CartaoDeCredito(
        id_ciclista=novo_ciclista.id,
        numero_cartao=request.cartao_de_credito.numero_cartao,
        nome_titular=request.cartao_de_credito.nome_titular,
        validade=request.cartao_de_credito.validade,
        cvv=request.cartao_de_credito.cvv
    )
    db.add(novo_cartao)
    db.commit()

    envia_email_cadastro(request.email)
    return novo_ciclista

def busca_ciclista_por_id(ciclista_id: int, db: Session) -> Ciclista:
    ciclista = db.query(Ciclista).filter(Ciclista.id == ciclista_id).first()
    if not ciclista:
        raise HTTPException(status_code=400, detail="Ciclista não encontrado")
    return ciclista

def atualiza_ciclista(ciclista_id: int, dados: CiclistaUpdate, db: Session) -> Ciclista:
    ciclista = db.query(Ciclista).filter(Ciclista.id == ciclista_id).first()
    if not ciclista:
        raise HTTPException(status_code=400, detail="Ciclista não encontrado")

    for attr, value in dados.model_dump(exclude_unset=True).items():
        setattr(ciclista, attr, value)

    db.commit()
    db.refresh(ciclista)
    return ciclista

def ativa_conta_service(ciclista_id: int, db: Session):
    ciclista = db.query(Ciclista).filter(Ciclista.id == ciclista_id).first()
    if not ciclista:
        raise HTTPException(status_code=400, detail="Ciclista não encontrado")

    ciclista.data_hora_confirmacao = datetime.today()
    ciclista.ativo = True
    db.commit()
    db.refresh(ciclista)
    return {"success": True}
