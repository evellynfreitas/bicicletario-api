from models import Cobranca
from datetime import datetime
from services.email import enviar_gmail

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
        return {"success": False, "detail": "Não foi encontrado nenhuma cobrança pendente"}

    for cobranca in cobrancas:
        email = 'evellyndfreitas@gmail.com'
        titulo = 'Nova Cobrança'
        mensagem = f'Nova cobrança! \nValor: {cobranca.valor}\nStatus: {cobranca.status}\nHora Solicitação: {cobranca.hora_solicitacao}'
        
        if enviar_gmail(email, titulo, mensagem):
            print("Email enviado")
        else:
            return {"success": False, "detail": "Não foi possível enviar o email"}
    
    return {"success": True, "detail": "Cobranças realizadas com sucesso"}
