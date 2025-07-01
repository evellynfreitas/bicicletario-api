import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session
from database import get_db
from main import app

# ---------- Fixtures e helpers ----------

@pytest.fixture
def test_client():
    return TestClient(app)

@pytest.fixture
def tranca_payload():
    return {
        "modelo": "Modelo 007",
        "ano_fabricacao": "2024",
        "localizacao": "Rio de Janeiro - RJ",
    }

@pytest.fixture
def update_payload():
    return {
        "numero": 1,
        "modelo": "Modelo 007",
        "ano_fabricacao": "2024",
        "localizacao": "Rio de Janeiro - RJ",
    }

@pytest.fixture
def override_get_db():
    db = MagicMock(spec=Session)

    def refresh_side_effect(obj):
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

def mock_response_success(detail, extra_data=None):
    base = {"success": True, "detail": detail}
    if extra_data:
        base.update(extra_data)
    return base

# ---------- Testes ----------

class TestTrancaRoutes:

    def test_criar_tranca_sucesso(self, test_client, tranca_payload, override_get_db):
        app.dependency_overrides[get_db] = override_get_db

        response = test_client.post("/tranca/", json=tranca_payload)

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["detail"] == "Nova tranca cadastrada com sucesso"

        app.dependency_overrides.clear()

    def test_editar_tranca_sucesso(self, test_client, update_payload):
        with patch("routers.tranca.editar_tranca") as mock:
            mock.return_value = mock_response_success("Tranca editada com sucesso")

            response = test_client.put("/tranca/", json=update_payload)

            assert response.status_code == 200
            assert response.json()["detail"] == "Tranca editada com sucesso"

    def test_retornar_tranca_sucesso(self, test_client):
        with patch("routers.tranca.retorna_tranca") as mock:
            mock.return_value = {
                "success": True,
                "tranca": {
                    "numero": 1,
                    "modelo": "Modelo 007",
                    "ano_fabricacao": "2024",
                    "localizacao": "Rio de Janeiro - RJ",
                    "status": "NOVA"
                }
            }

            response = test_client.get("/tranca/1")

            assert response.status_code == 200
            assert response.json()["numero"] == 1

    def test_deletar_tranca_sucesso(self, test_client):
        with patch("routers.tranca.deleta_tranca") as mock:
            mock.return_value = mock_response_success("Tranca removida com sucesso")

            response = test_client.delete("/tranca/1")

            assert response.status_code == 200
            assert response.json()["detail"] == "Tranca removida com sucesso"
