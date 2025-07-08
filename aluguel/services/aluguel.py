from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Aluguel, Ciclista
from datetime import datetime
from services.ciclista import busca_ciclista_por_id


def verifica_tranca():
    print("Tranca verificada")

def verifica_alugueis_ciclista(id_ciclista, db):
    aluguel = db.query(Aluguel).filter(Aluguel.id_ciclista == id_ciclista, Aluguel.hora_fim == None).all()
    print(aluguel)
    
    if aluguel:  # Verifica se a lista não está vazia
        return {"success": False, "detail": "Ciclista já tem um aluguel em aberto"}

    return {"success": True, "detail": "Ciclista está liberado para alugar nova bicicleta"}

def envia_email(email):
    print(f"Enviei o email de confirmação para {email}.")

def remove_bicicleta_da_tranca(id_bicicleta, id_tranca):
    print(f"Removi a bicicleta {id_bicicleta} da tranca {id_tranca}.")
    
def adiciona_bicicleta_na_tranca(id_bicicleta, id_tranca):
    print(f"Adicionei a bicicleta {id_bicicleta} na tranca {id_tranca}.")

def novo_aluguel(id_ciclista, id_bicicleta, id_tranca, db):
    ciclista = busca_ciclista_por_id(id_ciclista, db)
    if ciclista is None:
        return {"success": False, "detail": "Ciclista não encontrado"}
    
    if not ciclista.ativo:
        return {"success": False, "detail": "Ciclista não está com a conta ativada"}
    
    result = verifica_alugueis_ciclista(id_ciclista, db)
    if result['success'] == False:
        return result
    
    verifica_tranca()
    remove_bicicleta_da_tranca(id_bicicleta, id_tranca)
    
    aluguel = Aluguel(id_ciclista = id_ciclista, id_bicicleta = id_bicicleta, tranca_inicial=id_tranca)
    db.add(aluguel)
    db.commit()
    db.refresh(aluguel)
    
    envia_email(ciclista.email)
    
    return {"success": True, "detail": "Novo aluguel cadastrado com sucesso"}

def devolucao(id_bicicleta, id_tranca, db):
    aluguel = db.query(Aluguel).filter(Aluguel.id_bicicleta == id_bicicleta, Aluguel.hora_fim == None).first()

    if aluguel is None:
        return {"success": False, "detail": "Não encontrei um aluguel em andamento para essa bicicleta"}
    
    ciclista = busca_ciclista_por_id(aluguel.id_ciclista, db)
    if ciclista is None:
        return {"success": False, "detail": "Ciclista não encontrado"}
    
    adiciona_bicicleta_na_tranca(id_bicicleta, id_tranca)
    
    aluguel.hora_fim = datetime.today()
    
    db.add(aluguel)
    db.commit()
    db.refresh(aluguel)
    
    envia_email(aluguel.id_ciclista)
    
    return {"success": True, "detail": "Bicicleta devolvida com sucesso"}
 
