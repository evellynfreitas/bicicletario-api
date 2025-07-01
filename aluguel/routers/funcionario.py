from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import FuncionarioRequest, FuncionarioResponse, FuncionarioUpdate
from database import get_db
from services.funcionario import lista_funcionarios, cadastra_funcionario, edita_funcionario, retorna_funcionario, deleta_funcionario

router = APIRouter(prefix="/funcionario", tags=["funcionario"])

@router.get("/")
def retorna_funcionarios(db: Session = Depends(get_db)):
    return lista_funcionarios(db)

@router.post("/")
def cadastra(request: FuncionarioRequest, db: Session = Depends(get_db)):
    result = cadastra_funcionario(request, db)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["detail"])
    
    return result

@router.put("/")
def edita(request: FuncionarioUpdate, db: Session = Depends(get_db)):
    result = edita_funcionario(request, db)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["detail"])
    
    return result

@router.get("/{matricula}", response_model=FuncionarioResponse)
def retorna(matricula: int, db: Session = Depends(get_db)):
    result = retorna_funcionario(matricula, db)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["detail"])
    
    return result["funcionario"]

@router.delete("/{matricula}")
def deleta(matricula: int, db: Session = Depends(get_db)):
    result = deleta_funcionario(matricula, db)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["detail"])
    
    return result
