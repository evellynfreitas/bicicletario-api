from fastapi import APIRouter
from services.hello_service import get_hello_message

router = APIRouter()

@router.get("/hello")
def hello():
    return {"message": get_hello_message()}
