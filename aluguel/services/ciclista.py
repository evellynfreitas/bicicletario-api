from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from models import Ciclista, CartaoDeCredito
from schemas import CiclistaResponse, CiclistaUpdate
from database import get_db
import re
from datetime import datetime


def existe_email(email: str, db: Session) -> bool:
    ciclista = db.query(Ciclista).filter(Ciclista.email == email).first()
    if ciclista:
        return True
    else:
        return False

def email_valido(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def valida_documento(nacionalidade, cpf, passaporte):
    if nacionalidade.upper() in ['BRASILEIRA', 'BRASILEIRO']:
        if cpf is None:
            return False
    else:
        if passaporte is None:
            return False
    
    return True

def envia_email_cadastro(email):
    print("Enviei o email para o usuário!")


def valida_cartao(cartao):
    return True

def ativa_conta(id, db):
    ciclista = db.query(Ciclista).filter(Ciclista.id == id).first()
    if not ciclista:
        return False

    ciclista.data_hora_confirmacao = datetime.today()
    ciclista.ativo = True

    db.commit()
    db.refresh(ciclista)  
    return True

