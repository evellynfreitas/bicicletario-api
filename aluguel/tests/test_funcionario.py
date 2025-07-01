import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)

@pytest.fixture
def funcionario_payload():
    return {
        "nome": "João Silva",
        "email": "joao@example.com",
        "senha": "123456",
        "cpf": "12345678900",
        "data_nascimento": "1990-01-01",
        "funcao": "ADMINISTRADOR"
    }

@pytest.fixture
def funcionario_update_payload():
    return {
        "matricula": 1,
        "nome": "João Editado",
        "email": "joaoeditado@example.com",
        "senha": "nova123",
        "cpf": "09876543210",
        "data_nascimento": "1990-02-02",
        "funcao": "REPARADOR"
    }

# Cadastrar
def test_cadastrar_funcionario_sucesso(funcionario_payload):
    with patch("services.funcionario.cadastra_funcionario") as mock:
        mock.return_value = {"success": True, "detail": "Novo funcionário cadastrado com sucesso"}
        response = client.post("/funcionario/", json=funcionario_payload)

        assert response.status_code == 200
        assert response.json()["detail"] == "Novo funcionário cadastrado com sucesso"

# Retornar
def test_retornar_funcionario_sucesso():
    with patch("services.funcionario.retorna_funcionario") as mock:
        mock.return_value = {"success": True, "funcionario": {"nome": "João Silva"}}
        response = client.get("/funcionario/1")

        assert response.status_code == 200
        assert response.json()["nome"] == "João Silva"

# Editar
def test_edita_funcionario_sucesso(funcionario_update_payload):
    with patch("services.funcionario.edita_funcionario") as mock:
        mock.return_value = {"success": True, "detail": "Funcionário editado com sucesso"}
        response = client.put("/funcionario/", json=funcionario_update_payload)

        assert response.status_code == 200
        assert response.json()["detail"] == "Funcionário editado com sucesso"

# Deletar
def test_deletar_funcionario_sucesso():
    with patch("services.funcionario.deleta_funcionario") as mock:
        mock.return_value = {"success": True, "detail": "Funcionário removido com sucesso"}
        response = client.delete("/funcionario/1")

        assert response.status_code == 200
        assert response.json()["detail"] == "Funcionário removido com sucesso"

