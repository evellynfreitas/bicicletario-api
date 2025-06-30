from fastapi import APIRouter, HTTPException
from services.email import enviar_gmail

router = APIRouter(prefix="/email", tags=["email"])

@router.get("/enviar_email/")
def email_cadastrado(email: str, assunto: str, corpo:str):
    result = enviar_gmail(email, assunto, corpo)

    if result:
        return {"success": True}

    raise HTTPException(status_code=400, detail="Não foi possível enviar o email!")
