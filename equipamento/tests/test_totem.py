from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from database import get_db
from models import Totem
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

def test_criar_totem_sucesso(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    payload = {
        "localizacao": "Rio de Janeiro",
        "descricao": "Totem localizado no Rio de Janeiro",
    }

    response = client.post("/totem/", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["success"] == True
    assert data["detail"] == "Novo totem cadastrado com sucesso"
    
    app.dependency_overrides.clear()


@pytest.fixture
def update_payload():
    return {
        "numero": 1,
        "localizacao": "Rio de Janeiro",
        "descricao": "Totem localizado no Rio de Janeiro",
    }


def test_editar_totem_sucesso(update_payload):
    with patch("routers.totem.editar_totem") as mock:
        mock.return_value = {"success": True, "detail": "Totem editado com sucesso"}
        response = client.put("/totem/", json=update_payload)

        assert response.status_code == 200
        assert response.json()["detail"] == "Totem editado com sucesso"


def test_retornar_totem_sucesso():
    with patch("routers.totem.retorna_totem") as mock:
        mock.return_value = {"success": True, "totem": {"numero": 1, "localizacao": "Rio de Janeiro", "descricao": "Totem localizado no Rio de Janeiro"}}
        response = client.get("/totem/1")
        
        print(response.status_code)
        print(response.json())

        assert response.status_code == 200
        assert response.json()["numero"] == 1


def test_deletar_totem_sucesso():
    with patch("routers.totem.deleta_totem") as mock:
        mock.return_value = {"success": True, "detail": "Totem removido com sucesso"}
        response = client.delete("/totem/1")
        
        assert response.status_code == 200
        assert response.json()["detail"] == "Totem removido com sucesso"

