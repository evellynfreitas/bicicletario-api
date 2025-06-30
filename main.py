from fastapi import FastAPI
from controllers import hello_controller

app = FastAPI(
  title="bicicletario-api 🚴",
  description=("Sistema de Controle de Bicicletário"),
  version="1.0.0"
)
app.include_router(hello_controller.router)
