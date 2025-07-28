from models import Cobranca
from datetime import datetime
from services.email import enviar_gmail
from util import API_ALUGUEL_URL
import requests

def cadastrar_cobranca(request, db):
    try:
        nova_cobranca = Cobranca(
            ciclista=request.ciclista,
            valor=request.valor,
            status='PENDENTE'
        )
        db.add(nova_cobranca)
        db.commit()
        db.refresh(nova_cobranca)

        return {"success": True, "detail": "Nova cobrança cadastrada com sucesso"}

    except Exception as ex:
        print(ex)
        return {"success": False, "detail": "Não foi possível cadastrar a cobrança"}

def editar_cobranca(id_cobranca, status, db):
    cobranca = db.query(Cobranca).filter(Cobranca.id == id_cobranca).first()

    if cobranca is None:
        return {"success": False, "detail": "Cobrança não encontrada com esse ID"}
    
    if status not in ['PENDENTE', 'PAGA', 'CANCELADA']:
        return {"success": False, "detail": "Status de cobrança não reconhecido"}

    cobranca.status = status
    db.add(cobranca)
    db.commit()
    db.refresh(cobranca)

    return {"success": True, "detail": "Cobrança editada com sucesso"}

def retorna_cobranca(id_cobranca, db):
    cobranca = db.query(Cobranca).filter(Cobranca.id == id_cobranca).first()
    
    if cobranca is None:
        return {"success": False, "detail": "Cobrança não encontrada com esse ID"}

    return cobranca

def lista_cobrancas(db):
    cobranca = db.query(Cobranca).all()
    
    if cobranca is None:
        return {"success": False, "detail": "Não foi encontrada nenhuma cobrança"}

    return cobranca

def processa_cobrancas(db):
    cobrancas = db.query(Cobranca).filter(Cobranca.status == 'PENDENTE').all()
    
    if cobrancas is None:
        return {"success": True, "detail": "Não há nenhuma cobrança pendente"}

    for cobranca in cobrancas:
        response = requests.get(f"{API_ALUGUEL_URL}/ciclista/{cobranca.ciclista}")
        if response.ok:
            ciclista = response.json()
            email = ciclista.get("email")
        else:
            return {"success": False, "detail": f"Não foi possível encontrar o ciclista com id {cobranca.ciclista}"} 
        cobranca.status = 'PAGA'
        cobranca.hora_finalizacao = datetime.now()
        db.add(cobranca)
        titulo = 'Cobrança Paga'
        mensagem = f'Cobrança Paga! \nValor: {cobranca.valor}\nStatus: {cobranca.status}\nHora Solicitação: {cobranca.hora_solicitacao} \nHora Finalização: {cobranca.hora_finalizacao}'
        
        if enviar_gmail(email, titulo, mensagem):
            db.commit()
        else:
            return {"success": False, "detail": "Não foi possível enviar o email"}
    
    return {"success": True, "detail": "Cobranças realizadas com sucesso"}
