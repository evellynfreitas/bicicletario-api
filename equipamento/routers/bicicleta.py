from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import BicicletaRequest, BicicletaResponse, BicicletaUpdate
from database import get_db
from services.bicicleta import *

router = APIRouter(prefix="/bicicleta", tags=["bicicleta"])

@router.post("/")
def cadastra(request: BicicletaRequest, db: Session = Depends(get_db)):
    result = cadastrar_bicicleta(request, db)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["detail"])
    
    return result


@router.put("/")
def edita(request: BicicletaUpdate, db: Session = Depends(get_db)):
    result = editar_bicicleta(request, db)
    print(result)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["detail"])
    
    return result



