from models import Tranca
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





