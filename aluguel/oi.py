from database import SessionLocal
from models import Funcionario
from datetime import date

# Criar sessão com o banco
db = SessionLocal()

# Criar objeto Funcionario
novo_funcionario = Funcionario(
    nome="Evellyn",
    email="evellynfreitas@edu.unirio.br",
    cpf="12345678910",
    funcao="Reparador",
    senha="senha123",  # Ideal: usar hash da senha
    data_nascimento=date(1990, 5, 20)
)

# Adicionar e salvar no banco
db.add(novo_funcionario)
db.commit()
db.refresh(novo_funcionario)

print(f"Funcionário adicionado com matrícula {novo_funcionario.matricula}")

# Fechar a sessão
db.close()
