from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import CiclistaRequest, CiclistaResponse, CiclistaUpdate
from database import get_db
from services.ciclista import (
    verifica_email_cadastrado,
    cria_ciclista,
    busca_ciclista_por_id,
    atualiza_ciclista,
    ativa_conta_service
)

router = APIRouter(prefix="/ciclista", tags=["ciclista"])

@router.get("/existe_email/{email}")
def email_cadastrado(email: str, db: Session = Depends(get_db)):
    return verifica_email_cadastrado(email, db)

@router.post("/", response_model=CiclistaResponse)
def criar_ciclista_endpoint(request: CiclistaRequest, db: Session = Depends(get_db)):
    return cria_ciclista(request, db)

@router.get("/{ciclista_id}", response_model=CiclistaResponse)
def get_ciclista(ciclista_id: int, db: Session = Depends(get_db)):
    return busca_ciclista_por_id(ciclista_id, db)

@router.put("/{ciclista_id}", response_model=CiclistaResponse)
def update_ciclista(ciclista_id: int, dados: CiclistaUpdate, db: Session = Depends(get_db)):
    return atualiza_ciclista(ciclista_id, dados, db)

@router.get("/{ciclista_id}/ativar")
def ativa_conta_ciclista(ciclista_id: int, db: Session = Depends(get_db)):
    return ativa_conta_service(ciclista_id, db)
