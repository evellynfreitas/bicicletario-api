from models import Totem
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'equipamento')))

TOTEM_NAO_ENCONTRADO = "Totem não encontrado"

def cadastrar_totem(request, db):
    try:
        novo_totem = Totem(
            localizacao=request.localizacao,
            descricao=request.descricao,
        )
        db.add(novo_totem)
        db.commit()
        db.refresh(novo_totem)

        return {"success": True, "detail": "Novo totem cadastrado com sucesso"}

    except Exception:
        return {"success": False, "detail": "Não foi possível cadastrar o novo totem"}

def editar_totem(request, db):
    cadastro_totem = db.query(Totem).filter(Totem.numero == request.numero).first()

    if cadastro_totem is None:
        return {"success": False, "detail": TOTEM_NAO_ENCONTRADO}
    
    if request.localizacao:
        cadastro_totem.localizacao = request.localizacao
    
    if request.descricao:
        cadastro_totem.descricao = request.descricao 


    db.add(cadastro_totem)
    db.commit()
    db.refresh(cadastro_totem)

    return {"success": True, "detail": "Totem editado com sucesso"}

def retorna_totem(numero, db):
    totem = db.query(Totem).filter(Totem.numero == numero).first()
    if totem is None:
        return {"success": False, "detail": TOTEM_NAO_ENCONTRADO}
    
    return {"success": True, "detail": TOTEM_NAO_ENCONTRADO, "totem": totem}

def lista_totens(db):
    totens = db.query(Totem).all()
    return totens

def deleta_totem(numero, db):
    totem = db.query(Totem).filter(Totem.numero == numero).first()

    if totem is None:
        return {"success": False, "detail": TOTEM_NAO_ENCONTRADO}
    
    db.delete(totem)
    db.commit()
    
    return {"success": True, "detail": "Totem removido com sucesso"}
 