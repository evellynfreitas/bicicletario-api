from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.aluguel import verifica_alugueis_ciclista, novo_aluguel, resetar_banco_de_dados, devolucao

router = APIRouter(prefix="/aluguel", tags=["aluguel"])

@router.get("/verifica_alugueis_ciclista/")
def verificar_aluguel(id_ciclista: int, db: Session = Depends(get_db)):
    return verifica_alugueis_ciclista(id_ciclista, db)

@router.post("/")
def criar_aluguel(id_ciclista: int, id_bicicleta: int, id_tranca: int, db: Session = Depends(get_db)):
    return novo_aluguel(id_ciclista, id_bicicleta, id_tranca, db)

@router.post("/devolucao/")
def nova_devolucao(id_bicicleta: int, id_tranca: int, db: Session = Depends(get_db)):
    return devolucao(id_bicicleta, id_tranca, db)

@router.get("/restaurar_banco")
def restaurar_banco():
    resetar_banco_de_dados()
    return {"success": True, "detail": "Banco restaurado com sucesso"}
    
