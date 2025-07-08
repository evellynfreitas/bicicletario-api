from fastapi import APIRouter, HTTPException
from schemas import CartaoDeCreditoRequest
from services.cartao import valida_cartao
router = APIRouter(prefix="/cartao", tags=["cartao"])

@router.post("/validar")
def validar_cartao(cartao: CartaoDeCreditoRequest):
    result = valida_cartao(cartao)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["detail"])

    return result