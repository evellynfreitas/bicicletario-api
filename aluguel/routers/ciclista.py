from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Ciclista, CartaoDeCredito
from schemas import CiclistaRequest, CiclistaResponse, CiclistaUpdate
from database import get_db
from services.ciclista import *

router = APIRouter(prefix="/ciclista", tags=["ciclista"])

@router.get("/existe_email/{email}")
def email_cadastrado(email: str, db: Session = Depends(get_db)):
    return existe_email(email, db)

@router.post("/", response_model=CiclistaResponse)
def criar_ciclista(request: CiclistaRequest, db: Session = Depends(get_db)):
    if existe_email(request.email, db):
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    if not email_valido(request.email):
        raise HTTPException(status_code=400, detail="Email não é válido")
    
    if not valida_documento(request.nacionalidade, request.cpf, request.passaporte):
        raise HTTPException(status_code=400, detail="Documentos não preenchidos corretamente")
    
    if not valida_cartao(request.cartao_de_credito):
        raise HTTPException(status_code=400, detail="Cartão de crédito inválido")

    # Cria o ciclista
    novo_ciclista = Ciclista(
        nome=request.nome,
        email=request.email,
        nacionalidade=request.nacionalidade,
        senha=request.senha,
        cpf=request.cpf,
        passaporte=request.passaporte,
        data_nascimento=request.data_nascimento
    )
    db.add(novo_ciclista)
    db.commit()
    db.refresh(novo_ciclista)

    # Cria o cartão associado
    novo_cartao = CartaoDeCredito(
        id_ciclista=novo_ciclista.id,
        numero_cartao=request.cartao_de_credito.numero_cartao,
        nome_titular=request.cartao_de_credito.nome_titular,
        validade=request.cartao_de_credito.validade,
        cvv=request.cartao_de_credito.cvv
    )
    db.add(novo_cartao)
    db.commit()

    envia_email_cadastro(request.email)

    return novo_ciclista


@router.get("/{ciclista_id}", response_model=CiclistaResponse)
def get_ciclista(ciclista_id: int, db: Session = Depends(get_db)):
    ciclista = db.query(Ciclista).filter(Ciclista.id == ciclista_id).first()
    if not ciclista:
        raise HTTPException(status_code=400, detail="Ciclista não encontrado")
    return ciclista


@router.put("/{ciclista_id}", response_model=CiclistaResponse)
def update_ciclista(ciclista_id: int, dados: CiclistaUpdate, db: Session = Depends(get_db)):
    ciclista = db.query(Ciclista).filter(Ciclista.id == ciclista_id).first()
    if not ciclista:
        raise HTTPException(status_code=400, detail="Ciclista não encontrado")

    for attr, value in dados.model_dump(exclude_unset=True).items():
        setattr(ciclista, attr, value)

    db.commit()
    db.refresh(ciclista)
    return ciclista


@router.get("/{ciclista_id}/ativar")
def ativa_conta_ciclista(ciclista_id: int, db: Session = Depends(get_db)):
    if not ativa_conta(ciclista_id, db):
        raise HTTPException(status_code=400, detail="Ciclista não encontrado")
    else:
        return {"success": True}