from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import TrancaRequest, TrancaResponse, TrancaUpdate
from database import get_db
from services.tranca import cadastrar_tranca, editar_tranca, lista_trancas, retorna_tranca, deleta_tranca, inserir_bicicleta_tranca, remover_bicicleta, incluir_tranca_totem, novo_reparo, solicitar_reparo

router = APIRouter(prefix="/tranca", tags=["tranca"])

@router.post("/")
def cadastra(request: TrancaRequest, db: Session = Depends(get_db)):
    result = cadastrar_tranca(request, db)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["detail"])
    
    return result


@router.put("/")
def edita(request: TrancaUpdate, db: Session = Depends(get_db)):
    result = editar_tranca(request, db)
    print(result)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["detail"])
    
    return result

@router.get("/")
def lista(db: Session = Depends(get_db)):
    return lista_trancas(db)

@router.get("/{numero}", response_model=TrancaResponse)
def retorna(numero: int, db: Session = Depends(get_db)):
    result = retorna_tranca(numero, db)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["detail"])
    
    return result["tranca"]

@router.delete("/{numero}")
def deleta(numero: int, db: Session = Depends(get_db)):
    result = deleta_tranca(numero, db)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["detail"])
    
    return result

@router.post("/insere_bicicleta")
def inserir_bicicleta(id_bicicleta: int, id_tranca: int, id_funcionario: int, db: Session = Depends(get_db)):
    result = inserir_bicicleta_tranca(id_bicicleta, id_tranca, id_funcionario, db)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["detail"])
    
    return result

@router.post("/remover_bicicleta")
def remover_bicicleta_tranca(id_bicicleta: int, id_funcionario: int, tipo_reparo: str, db: Session = Depends(get_db)):
    result = remover_bicicleta(id_bicicleta, id_funcionario, tipo_reparo, db)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["detail"])
    
    return result

@router.post("/inserir_totem")
def inserir_tranca(id_tranca: int, id_funcionario: int, id_totem: int, db: Session = Depends(get_db)):
    result = incluir_tranca_totem(id_tranca, id_funcionario, id_totem, db)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["detail"])
    
    return result

@router.post("/reparo")
def reparo(id_tranca: int, id_funcionario: int, db: Session = Depends(get_db)):
    result = novo_reparo(id_tranca, id_funcionario, db)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["detail"])
    
    return result

@router.post("/solicitar_reparo")
def solicita_reparo_tranca(id_tranca: int, db: Session = Depends(get_db)):
    result = solicitar_reparo(id_tranca, db)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["detail"])
    
    return result

