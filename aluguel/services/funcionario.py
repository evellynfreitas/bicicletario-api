from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from models import Funcionario
from database import get_db
import re
from datetime import datetime


def existe_email(email: str, db: Session) -> bool:
    cadastrado = db.query(Funcionario).filter(Funcionario.email == email).first()
    if cadastrado:
        return True
    else:
        return False

def email_valido(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def envia_email_cadastro(email):
    print("Enviei o email para o usuário!")

def cadastra_funcionario(funcionario, db):
    if existe_email(funcionario.email, db):
        return {"success": False, "detail": "Email já cadastrado"}

    if not email_valido(funcionario.email):
        return {"success": False, "detail": "Email invalido"}
    
    if funcionario.funcao.upper() not in ['ADMINISTRADOR', 'REPARADOR']:
        return {"success": False, "detail": "Função não reconhecida"}
    
    novo_funcionario = Funcionario(
        nome=funcionario.nome,
        email=funcionario.email,
        senha=funcionario.senha,
        cpf=funcionario.cpf,
        data_nascimento=funcionario.data_nascimento,
        funcao=funcionario.funcao
    )
    db.add(novo_funcionario)
    db.commit()
    db.refresh(novo_funcionario)

    return {"success": True, "detail": "Novo funcionário cadastrado com sucesso"}


def edita_funcionario(funcionario, db):
    cadastro_funcionario = db.query(Funcionario).filter(Funcionario.matricula == funcionario.matricula).first()

    if cadastro_funcionario is None:
        return {"success": False, "detail": "Funcionário não encontrado"}
    
    if funcionario.nome:
        cadastro_funcionario.nome = funcionario.nome
    
    if funcionario.funcao:
        if funcionario.funcao.upper() not in ['ADMINISTRADOR', 'REPARADOR']:
            return {"success": False, "detail": "Função não reconhecida"}
        cadastro_funcionario.funcao = funcionario.funcao
    
    if funcionario.cpf:
        cadastro_funcionario.cpf = funcionario.cpf 

    if funcionario.email:
        if existe_email(funcionario.email, db):
            return {"success": False, "detail": "Email já cadastrado"}

        if not email_valido(funcionario.email):
            return {"success": False, "detail": "Email invalido"}
        
        cadastro_funcionario.email = funcionario.email

    if funcionario.senha:
        cadastro_funcionario.senha = funcionario.senha 

    if funcionario.data_nascimento:
        cadastro_funcionario.data_nascimento = funcionario.data_nascimento 


    db.add(cadastro_funcionario)
    db.commit()
    db.refresh(cadastro_funcionario)

    return {"success": True, "detail": "Funcionário editado com sucesso"}


def retorna_funcionario(matricula, db):
    funcionario = db.query(Funcionario).filter(Funcionario.matricula == matricula).first()
    if funcionario is None:
        return {"success": False, "detail": "Funcionário não encontrado"}
    
    return {"success": True, "detail": "Funcionário não encontrado", "funcionario": funcionario}


def lista_funcionarios(db):
    funcionarios = db.query(Funcionario).all()
    return funcionarios


def deleta_funcionario(matricula, db):
    funcionario = db.query(Funcionario).filter(Funcionario.matricula == matricula).first()

    if funcionario is None:
        return {"success": False, "detail": "Funcionário não encontrado"}
    
    db.delete(funcionario)
    db.commit()
    
    return {"success": True, "detail": "Funcionário removido com sucesso"}


