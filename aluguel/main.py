from fastapi import FastAPI
from routers import ciclista, funcionario
from database import engine, Base

app = FastAPI(
    title="API de Aluguel de Bicicletas",
    description="API",
    version="1.0.0"
)

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app.include_router(ciclista.router)
app.include_router(funcionario.router)

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API de Aluguel"}