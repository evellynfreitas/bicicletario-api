from models import Bicicleta
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'equipamento')))

def cadastrar_bicicleta(request, db):
    try:
        nova_bicicleta = Bicicleta(
            marca=request.marca,
            modelo=request.modelo,
            ano=request.ano
        )
        db.add(nova_bicicleta)
        db.commit()
        db.refresh(nova_bicicleta)

        return {"success": True, "detail": "Nova bicicleta cadastrada com sucesso"}

    except Exception:
        return {"success": False, "detail": "Não foi possível cadastrar a nova bicicleta"}

def editar_bicicleta(request, db):
    cadastro_bicicleta = db.query(Bicicleta).filter(Bicicleta.numero == request.numero).first()

    if cadastro_bicicleta is None:
        return {"success": False, "detail": "Bicicleta não encontrada"}
    
    if request.marca:
        cadastro_bicicleta.marca = request.marca
    
    if request.modelo:
        cadastro_bicicleta.modelo = request.modelo 

    if request.ano:
        cadastro_bicicleta.ano = request.ano 


    db.add(cadastro_bicicleta)
    db.commit()
    db.refresh(cadastro_bicicleta)

    return {"success": True, "detail": "Bicicleta editada com sucesso"}

def retorna_bicicleta(numero, db):
    bicicleta = db.query(Bicicleta).filter(Bicicleta.numero == numero).first()
    if bicicleta is None:
        return {"success": False, "detail": "Bicicleta não encontrado"}
    
    return {"success": True, "detail": "Bicicleta encontrada", "bicicleta": bicicleta}


def lista_bicicletas(db):
    bicicletas = db.query(Bicicleta).all()
    return bicicletas


def deleta_bicicleta(numero, db):
    bicicleta = db.query(Bicicleta).filter(Bicicleta.numero == numero).first()

    if bicicleta is None:
        return {"success": False, "detail": "Bicicleta não encontrada"}
    
    db.delete(bicicleta)
    db.commit()
    
    return {"success": True, "detail": "Bicicleta removida com sucesso"}





