from models import Tranca, Bicicleta, ReparoTranca, ReparoBicicleta
from datetime import datetime
from util import API_EXTERNO_URL, API_ALUGUEL_URL
import requests
import sys
import os

TRANCA_NAO_ENCONTRADA = "Tranca não encontrada"
EM_REPARO = "EM REPARO"

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'equipamento')))

def envia_email(email, titulo, corpo):
    params = {
        "email": email,
        "assunto": titulo, 
        "corpo": corpo
    }

    response = requests.get(f"{API_EXTERNO_URL}/email/enviar_email/", params=params)
    
    if response.ok:
        return True

    else:
        return False
    
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

def incluir_tranca_totem(numero_tranca, funcionario_id, totem_id, db):
    tranca = db.query(Tranca).filter(Tranca.numero == numero_tranca).first()
    if not tranca:
        return {"success": False, "detail": TRANCA_NAO_ENCONTRADA}

    if tranca.status not in ["NOVA", EM_REPARO]:
        return {"success": False, "detail": "Tranca não está apta para inclusão no totem"}

    if tranca.status == EM_REPARO:
        reparo = (db.query(ReparoTranca).filter(ReparoTranca.tranca_numero == numero_tranca).order_by(ReparoTranca.data_retirada.desc()).first())
        if not reparo or reparo.funcionario_id != funcionario_id:
            return {"success": False, "detail": "Funcionário não autorizado a devolver esta tranca (reparo foi iniciado por outro)"}
        
        reparo.data_retorno = datetime.now()

    funcionario = requests.get("{API_ALUGUEL_URL}/funcionario/{funcionario_id}")
    funcionario = funcionario.json()

    tranca.status = "DISPONIVEL"
    tranca.id_totem = totem_id
    
    mensagem = f"""
        A tranca {numero_tranca} foi inserida com sucesso no totem {totem_id} às {datetime.now()}.
    """

    if envia_email(funcionario.email, "Tranca inserida", mensagem):
        db.commit()
        return {"success": True, "detail": "Tranca incluída com sucesso no totem."}
    else:
        return {"success": False, "detail": "Não foi possível enviar o email para o funcionário."}

def novo_reparo(numero_tranca, funcionario_id, db):

    tranca = db.query(Tranca).filter(Tranca.numero == numero_tranca).first()
    if not tranca:
        return {"success": False, "detail": TRANCA_NAO_ENCONTRADA}

    if tranca.status != "REPARO SOLICITADO":
        return {"success": False, "detail": "A tranca não está com status 'reparo solicitado'"}

    if tranca.bicicleta_numero is not None:
        return {"success": False, "detail": "A tranca ainda possui uma bicicleta acoplada"}

    tranca.status = EM_REPARO
    tranca.id_totem = None

    reparo = ReparoTranca(tranca_numero=numero_tranca, funcionario_id=funcionario_id, data_retirada=datetime.now())
    db.add(reparo)

    funcionario = requests.get("{API_ALUGUEL_URL}/funcionario/{funcionario_id}")
    funcionario = funcionario.json()
    
    mensagem = f"""
        A tranca {numero_tranca} foi retirada para reparo.
    """

    if envia_email(funcionario.email, "Reparo Tranca", mensagem):
        db.commit()
        return {"success": True, "detail": "Tranca foi removida para reparo."}
    else:
        return {"success": False, "detail": "Não foi possível enviar o email para o funcionário."}

def inserir_bicicleta_tranca(numero_bicicleta, numero_tranca, funcionario_id, db):
    bicicleta = db.query(Bicicleta).filter(Bicicleta.numero == numero_bicicleta).first()
    if not bicicleta:
        return {"success": False, "detail": "Bicicleta não encontrada"}
    
    if bicicleta.status not in ["NOVA", EM_REPARO]:
        return {"success": False, "detail": "Status da bicicleta inválido para inclusão"}

    tranca = db.query(Tranca).filter(Tranca.numero == numero_tranca).first()
    if not tranca:
        return {"success": False, "detail": TRANCA_NAO_ENCONTRADA}

    if tranca.status != "DISPONIVEL":
        return {"success": False, "detail": "Tranca não está disponível"}

    if bicicleta.status == EM_REPARO:
        reparo = (
            db.query(ReparoBicicleta)
            .filter(ReparoBicicleta.bicicleta_numero == numero_bicicleta)
            .order_by(ReparoBicicleta.data_retirada.desc())
            .first()
        )
        
        if not reparo or reparo.funcionario_id != funcionario_id:
            return {"success": False, "detail": "Funcionário não autorizado a devolver esta bicicleta"}
            
        reparo.data_retorno = datetime.now()

    tranca.bicicleta_numero = numero_bicicleta
    bicicleta.status = "DISPONIVEL"
    bicicleta.localizacao = f"Totem {tranca.id_totem} - Tranca {numero_tranca}"

    funcionario = requests.get("{API_ALUGUEL_URL}/funcionario/{funcionario_id}")
    funcionario = funcionario.json()
    
    mensagem = f"""
        A bicicleta {bicicleta.id} foi inserida com sucesso na tranca {numero_tranca}.
    """

    if envia_email(funcionario.email, "Inserção Bicicleta", mensagem):
        db.commit()
        return {"success": True, "detail": "Bicicleta inserida com sucesso na tranca"}
    else:
        return {"success": False, "detail": "Não foi possível enviar o email para o funcionário."}

def remover_bicicleta(numero_tranca, funcionario_id, tipo_retirada, db):
    tranca = db.query(Tranca).filter(Tranca.numero == numero_tranca).first()
    if not tranca:
        return {"success": False, "detail": TRANCA_NAO_ENCONTRADA}

    if not tranca.bicicleta_numero:
        return {"success": False, "detail": "Tranca não possui bicicleta presa"}

    bicicleta = db.query(Bicicleta).filter(Bicicleta.numero == tranca.bicicleta_numero).first()

    if tipo_retirada == "REPARO":
        if bicicleta.status != "REPARO SOLICITADO":
            return {"success": False, "detail": "Bicicleta não está com status 'reparo solicitado'"}

    elif tipo_retirada == "APOSENTADORIA":
        if bicicleta.status == "EM USO":
            return {"success": False, "detail": "Não é possível aposentar bicicleta em uso"}
    else:
        return {"success": False, "detail": "Tipo de retirada inválido. Use 'reparo' ou 'aposentadoria'"}

    tranca.bicicleta_numero = None
    if tipo_retirada == "REPARO":
        bicicleta.status = EM_REPARO
    else:
        bicicleta.status = "APOSENTADA"

    bicicleta.localizacao = "Oficina" if tipo_retirada == "REPARO" else "Baixada"

    if tipo_retirada == "REPARO":
        reparo = ReparoBicicleta(bicicleta_numero=bicicleta.numero, funcionario_id=funcionario_id, data_retirada=datetime.now())
        db.add(reparo)

    funcionario = requests.get("{API_ALUGUEL_URL}/funcionario/{funcionario_id}")
    funcionario = funcionario.json()
    
    mensagem = f"""
        A bicicleta {bicicleta.id} foi removida da tranca {numero_tranca} para {tipo_retirada}.
    """

    if envia_email(funcionario.email, "Remoção Bicicleta", mensagem):
        db.commit()
        return {"success": True, "detail": f"Bicicleta retirada com sucesso para {tipo_retirada}."}
    else:
        return {"success": False, "detail": "Não foi possível enviar o email para o funcionário."}


def solicitar_reparo(id_tranca, db):
    tranca = retorna_tranca(id_tranca, db)['tranca']
    tranca.status = 'REPARO SOLICITADO'
    db.add(tranca)
    db.commit()
    
    return {"success": True, "detail": "Reparo solicitado com sucesso"}
