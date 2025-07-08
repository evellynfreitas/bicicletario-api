from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import TotemRequest, TotemResponse, TotemUpdate, BicicletaRequest
from database import get_db
from services.totem import cadastrar_totem, editar_totem, lista_totens, retorna_totem, deleta_totem

router = APIRouter(prefix="/totem", tags=["totem"])

@router.post("/")
def cadastra(request: TotemRequest, db: Session = Depends(get_db)):
    result = cadastrar_totem(request, db)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["detail"])
    
    return result


@router.put("/")
def edita(request: TotemUpdate, db: Session = Depends(get_db)):
    result = editar_totem(request, db)
    print(result)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["detail"])
    
    return result

@router.get("/")
def lista(db: Session = Depends(get_db)):
    return lista_totens(db)

@router.get("/{numero}", response_model=TotemResponse)
def retorna(numero: int, db: Session = Depends(get_db)):
    result = retorna_totem(numero, db)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["detail"])
    
    return result["totem"]

@router.delete("/{numero}")
def deleta(numero: int, db: Session = Depends(get_db)):
    result = deleta_totem(numero, db)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["detail"])
    
    return result
