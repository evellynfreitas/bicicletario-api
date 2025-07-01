from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from database import get_db
from main import app
import pytest

client = TestClient(app)

@pytest.fixture
def override_get_db():
    db = MagicMock(spec=Session)

    def refresh_side_effect(obj):
        # Simula o que seria preenchido após o db.refresh()
        obj.id = 1
        obj.ativo = True
        return obj

    db.add.return_value = None
    db.commit.return_value = None
    db.refresh.side_effect = refresh_side_effect
    db.query().filter().first.return_value = None

    def _get_db():
        return db

    return _get_db

def test_criar_ciclista_sucesso(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    payload = {
        "nome": "Maria Silva",
        "email": "maria@example.com",
        "nacionalidade": "Brasileira",
        "senha": "senhasegura",
        "cpf": "12345678900",
        "data_nascimento": "1990-05-15",
        "cartao_de_credito": {
            "numero_cartao": "1234123412341234",
            "nome_titular": "Maria Silva",
            "validade": "2026-12-31",
            "cvv": "123"
        }
    }

    response = client.post("/ciclista/", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["nome"] == "Maria Silva"
    assert data["email"] == "maria@example.com"
    assert data["ativo"] is True
    assert "id" in data
    app.dependency_overrides.clear()


@pytest.fixture
def override_get_db_com_email_existente():
    db = MagicMock(spec=Session)

    def refresh_side_effect(obj):
        obj.id = 1
        obj.ativo = True
        return obj

    db.add.return_value = None
    db.commit.return_value = None
    db.refresh.side_effect = refresh_side_effect

    # Simula que já existe um ciclista com esse e-mail
    db.query().filter().first.return_value = MagicMock()  # algo truthy

    def _get_db():
        return db

    return _get_db

def test_nao_deve_criar_ciclista_com_email_duplicado(override_get_db_com_email_existente):
    app.dependency_overrides[get_db] = override_get_db_com_email_existente
    client = TestClient(app)

    payload = {
        "nome": "Maria Silva",
        "email": "maria@example.com",  # já cadastrado
        "nacionalidade": "Brasileira",
        "senha": "senhasegura",
        "cpf": "12345678900",
        "data_nascimento": "1990-05-15",
        "cartao_de_credito": {
            "numero_cartao": "1234123412341234",
            "nome_titular": "Maria Silva",
            "validade": "2026-12-31",
            "cvv": "123"
        }
    }

    response = client.post("/ciclista/", json=payload)
    print(response.status_code)
    print(response.json())
    assert response.status_code == 400
    assert response.json()["detail"] == "Email já cadastrado"
    app.dependency_overrides.clear()


def test_erro_quando_brasileira_sem_cpf(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    payload = {
        "nome": "João",
        "email": "joao@example.com",
        "nacionalidade": "Brasileiro",
        "senha": "senha123",
        "cpf": None,
        "data_nascimento": "1990-01-01",
        "cartao_de_credito": {
            "numero_cartao": "4111111111111111",
            "nome_titular": "João",
            "validade": "2026-12-31",
            "cvv": "123"
        }
    }

    response = client.post("/ciclista/", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Documentos não preenchidos corretamente"
    app.dependency_overrides.clear()


def test_erro_quando_estrangeiro_sem_passaporte(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    payload = {
        "nome": "Ana",
        "email": "ana@example.com",
        "nacionalidade": "Argentina",
        "senha": "senha123",
        "passaporte": None,
        "data_nascimento": "1990-01-01",
        "cartao_de_credito": {
            "numero_cartao": "4111111111111111",
            "nome_titular": "Ana",
            "validade": "2026-12-31",
            "cvv": "123"
        }
    }

    response = client.post("/ciclista/", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Documentos não preenchidos corretamente"
    app.dependency_overrides.clear()



def test_erro_quando_email_invalido(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    payload = {
        "nome": "Carlos",
        "email": "email-invalido.com",  # <-- inválido
        "nacionalidade": "Brasileira",
        "senha": "senha123",
        "cpf": "12345678900",
        "data_nascimento": "1990-01-01",
        "cartao_de_credito": {
            "numero_cartao": "4111111111111111",
            "nome_titular": "Carlos",
            "validade": "2026-12-31",
            "cvv": "123"
        }
    }

    response = client.post("/ciclista/", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email não é válido"
    app.dependency_overrides.clear()



def test_ativar_conta_rota_sucesso():
    db = MagicMock()
    fake_ciclista = MagicMock()
    db.query().filter().first.return_value = fake_ciclista

    def _get_db():
        return db

    app.dependency_overrides[get_db] = _get_db
    client = TestClient(app)

    response = client.get("/ciclista/1/ativar")

    assert response.status_code == 200
    assert response.json() == {"success": True}

    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(fake_ciclista)

    app.dependency_overrides.clear()


def test_ativar_conta_rota_falha():
    db = MagicMock()
    db.query().filter().first.return_value = None  # simula não encontrado

    def _get_db():
        return db

    app.dependency_overrides[get_db] = _get_db
    client = TestClient(app)

    response = client.get("/ciclista/999/ativar")

    assert response.status_code == 400
    assert response.json()["detail"] == "Ciclista não encontrado"

    db.commit.assert_not_called()
    app.dependency_overrides.clear()

