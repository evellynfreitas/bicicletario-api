from schemas import CobrancaRequest, CobrancaResponse
from services.cobranca import cadastrar_cobranca, editar_cobranca, retorna_cobranca, lista_cobrancas, processa_cobrancas
from sqlalchemy.orm import Session
from database import get_db
from fastapi import APIRouter, HTTPException, Depends

router = APIRouter(prefix="/cobranca", tags=["cobranca"])

@router.post("/")
def cadastra(request: CobrancaRequest, db: Session = Depends(get_db)):
    result = cadastrar_cobranca(request, db)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["detail"])
    
    return result


@router.put("/")
def edita(id_cobranca: int, status: str, db: Session = Depends(get_db)):
    result = editar_cobranca(id_cobranca, status, db)
    print(result)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["detail"])
    
    return result


@router.get("/{id}", response_model=CobrancaResponse)
def retorna(id: int, db: Session = Depends(get_db)):
    result = retorna_cobranca(id, db)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["detail"])
    
    return result["bicicleta"]


@router.get("/")
def lista(db: Session = Depends(get_db)):
    return lista_cobrancas(db)


@router.get("/fila_cobranca/processa")
def lista(db: Session = Depends(get_db)):
    result = processa_cobrancas(db)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["detail"])
    
    return result

