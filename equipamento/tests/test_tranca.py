from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
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

def test_criar_tranca_sucesso(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    payload = {
        "modelo": "Modelo 007",
        "ano_fabricacao": "2024",
        "localizacao": "Rio de Janeiro - RJ",
    }

    response = client.post("/tranca/", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert data["detail"] == "Nova tranca cadastrada com sucesso"
    
    app.dependency_overrides.clear()


@pytest.fixture
def update_payload():
    return {
        "numero": 1,
        "modelo": "Modelo 007",
        "ano_fabricacao": "2024",
        "localizacao": "Rio de Janeiro - RJ",
    }


def test_editar_tranca_sucesso(update_payload):
    with patch("routers.tranca.editar_tranca") as mock:
        mock.return_value = {"success": True, "detail": "Tranca editada com sucesso"}
        response = client.put("/tranca/", json=update_payload)

        assert response.status_code == 200
        assert response.json()["detail"] == "Tranca editada com sucesso"


def test_retornar_tranca_sucesso():
    with patch("routers.tranca.retorna_tranca") as mock:
        mock.return_value = {"success": True, "tranca": {"numero": 1, "modelo": "Modelo 007", "ano_fabricacao": "2024", "localizacao": "Rio de Janeiro - RJ", "status": "NOVA" }}
        response = client.get("/tranca/1")
        
        assert response.status_code == 200
        assert response.json()["numero"] == 1


def test_deletar_tranca_sucesso():
    with patch("routers.tranca.deleta_tranca") as mock:
        mock.return_value = {"success": True, "detail": "Tranca removida com sucesso"}
        response = client.delete("/tranca/1")

        assert response.status_code == 200
        assert response.json()["detail"] == "Tranca removida com sucesso"

