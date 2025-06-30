from fastapi import FastAPI
from routers import email

app = FastAPI(
    title="API Externa",
    description="API Externa",
    version="1.0.0"
)

# Cria as tabelas no banco de dados
# Base.metadata.create_all(bind=engine)

app.include_router(email.router)

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API Externa"}