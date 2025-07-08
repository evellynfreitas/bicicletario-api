from models import Tranca, Bicicleta, Reparo
from datetime import datetime
from util import API_EXTERNO_URL, API_ALUGUEL_URL
import requests
import httpx
import sys
import os

TRANCA_NAO_ENCONTRADA = "Tranca não encontrada"

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'equipamento')))

def cadastrar_tranca(request, db):
    try:
        nova_tranca = Tranca(
            modelo=request.modelo,
            ano_fabricacao=request.ano_fabricacao,
            localizacao=request.localizacao
        )
        db.add(nova_tranca)
        db.commit()
        db.refresh(nova_tranca)

        return {"success": True, "detail": "Nova tranca cadastrada com sucesso"}

    except Exception:
        return {"success": False, "detail": "Não foi possível cadastrar a nova tranca"}

def editar_tranca(request, db):
    cadastro_tranca = db.query(Tranca).filter(Tranca.numero == request.numero).first()

    if cadastro_tranca is None:
        return {"success": False, "detail": TRANCA_NAO_ENCONTRADA}
    
    if request.modelo:
        cadastro_tranca.modelo = request.modelo
    
    if request.ano_fabricacao:
        cadastro_tranca.ano_fabricacao = request.ano_fabricacao 

    if request.localizacao:
        cadastro_tranca.localizacao = request.localizacao 


    db.add(cadastro_tranca)
    db.commit()
    db.refresh(cadastro_tranca)

    return {"success": True, "detail": "Tranca editada com sucesso"}

def retorna_tranca(numero, db):
    tranca = db.query(Tranca).filter(Tranca.numero == numero).first()
    if tranca is None:
        return {"success": False, "detail": TRANCA_NAO_ENCONTRADA}
    
    return {"success": True, "detail": "Tranca encontrada", "tranca": tranca}


def lista_trancas(db):
    trancas = db.query(Tranca).all()
    return trancas


def deleta_tranca(numero, db):
    tranca = db.query(Tranca).filter(Tranca.numero == numero).first()

    if tranca is None:
        return {"success": False, "detail": TRANCA_NAO_ENCONTRADA}
    
    db.delete(tranca)
    db.commit()
    
    return {"success": True, "detail": "Tranca removida com sucesso"}

def retorna_funcionario(id_funcionario):
    response = requests.get(f"{API_ALUGUEL_URL}/funcionario/{id_funcionario}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

def enviar_email(params):

    response = requests.get(f"{API_EXTERNO_URL}/email/enviar_email/", params=params)

    if response.status_code == 200:
        print("Email enviado com sucesso:", response.json())
        return True
    else:
        print("Erro ao enviar email:", response.text)
        return False

def inserir_bicicleta_tranca(id_bicicleta, id_tranca, id_funcionario, db):
    bicicleta = db.query(Bicicleta).filter(Bicicleta.numero == id_bicicleta).first()
    tranca = db.query(Tranca).filter(Tranca.numero == id_tranca).first()

    if bicicleta is None:
        return {"success": False, "detail": "Bicicleta não encontrada com esse id"}
    
    if bicicleta.status not in ["NOVA", "EM REPARO"]:
        return {"success": False, "detail": f"Não é possível inserir essa bicicleta com o status {bicicleta.status}"}
    
    if tranca is None:
        return {"success": False, "detail": "Tranca não encontrada com esse id"}
    
    if tranca.status not in ("DISPONIVEL", "NOVA"):
        return {"success": False, "detail": f"Não é possível inserir uma bicicleta nessa tranca com status {tranca.status}"}

    if bicicleta.status == 'EM REPARO':
        reparo = (
            db.query(Reparo)
            .filter(Reparo.bicicleta_numero == id_bicicleta)
            .filter(Reparo.data_retorno.is_(None))
            .order_by(Reparo.data_retirada.desc())
            .first()
        )

        if reparo is None:
            return {"success": False, "detail": f"Não foi encontrado o registro de reparo dessa bicicleta"}
        
        funcionario = retorna_funcionario(id_funcionario)
        if reparo.funcionario_id != id_funcionario:
            return {"success": False, "detail": f"Somente o funcionário responsável por esse reparo pode devolver esta bicicleta"}

        reparo.data_retorno = datetime.today()
        db.add(reparo)
        
        params = {
            "assunto": "Reparo Concluído",
            "email": funcionario.email,
            "corpo": f"""Reparo da bicicleta concluído"""
        }
        
        enviar_email(params)
        
    tranca.bicicleta_numero = bicicleta.numero
    bicicleta.status = 'DISPONIVEL'
    db.add(tranca)
    db.add(bicicleta)
    db.commit()

    return {"success": True, "detail": f"Bicicleta foi inserida com sucesso na tranca"}

def remover_bicicleta_reparo(id_bicicleta, id_funcionario, tipo_reparo, db):
    bicicleta = db.query(Bicicleta).filter(Bicicleta.numero == id_bicicleta).first()
    tranca = db.query(Tranca).filter(Tranca.bicicleta_numero == id_bicicleta).first()

    if bicicleta is None:
        return {"success": False, "detail": "Bicicleta não encontrada com esse id"}
    
    if bicicleta.status not in ["REPARO SOLICITADO"]:
        return {"success": False, "detail": "Essa bicicleta não está com reparo solicitado"}
    
    if tranca is None:
        return {"success": False, "detail": "Bicicleta não está adicionada corretamente a uma tranca"}
    
    if tipo_reparo not in ["REPARO", "APOSENTADORIA"]:
        return {"success": False, "detail": "Tipo de reparo não reconhecido"}

    tranca.bicicleta_numero = None
    
    if tipo_reparo == 'REPARO':
        bicicleta.status = 'EM REPARO'
    else:
        bicicleta.status = 'APOSENTADA'
    
    funcionario = retorna_funcionario(id_funcionario)
    reparo = Reparo()
    reparo.bicicleta_numero = bicicleta.numero
    reparo.funcionario_id = id_funcionario

    db.add(tranca)
    db.add(reparo)
    db.add(bicicleta)
    db.commit()

    if funcionario:
        params = {
            "assunto": "Reparo Iniciado",
            "email": funcionario.get('email'),
            "corpo": f"""Reparo da bicicleta foi iniciado no dia {reparo.data_retirada}.
                
            Dados:
            Número da bicicleta: {bicicleta.numero}
            Marca: {bicicleta.marca}
            Modelo: {bicicleta.modelo}
            Status: {bicicleta.status}"""
        }
            
        enviar_email(params)
   
    return {"success": True, "detail": "Bicicleta retirada para reparo com sucesso"}

