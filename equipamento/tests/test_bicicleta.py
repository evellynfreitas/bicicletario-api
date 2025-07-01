from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from database import get_db
from models import Bicicleta
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

def test_criar_bicicleta_sucesso(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    payload = {
        "marca": "Truk",
        "modelo": "Modelo 007",
        "ano": "2024"
    }

    response = client.post("/bicicleta/", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["success"] == True
    assert data["detail"] == "Nova bicicleta cadastrada com sucesso"
    
    app.dependency_overrides.clear()


@pytest.fixture
def update_payload():
    return {
        "numero": 1,
        "marca": "Renault",
        "modelo": "Novo modelo",
        "ano": "2025",
    }


def test_edita_bicicleta_sucesso(update_payload):
    with patch("routers.bicicleta.editar_bicicleta") as mock:
        mock.return_value = {"success": True, "detail": "Bicicleta editada com sucesso"}
        response = client.put("/bicicleta/", json=update_payload)

        print(response.status_code)
        print(response.json())

        assert response.status_code == 200
        assert response.json()["detail"] == "Bicicleta editada com sucesso"

