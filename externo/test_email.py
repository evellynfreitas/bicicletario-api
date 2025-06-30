# tests/test_email.py
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app  # Altere para o caminho real do seu app se necessário

client = TestClient(app)

def test_enviar_email_sucesso():
    with patch("services.email.enviar_gmail") as mock_enviar_email:
        mock_enviar_email.return_value = True

        response = client.get("/email/enviar_email/", params={
            "email": "evellynfreitas@edu.unirio.br",
            "assunto": "Assunto Teste",
            "corpo": "Corpo do email"
        })

        assert response.status_code == 200
        assert response.json() == {"success": True}


def test_enviar_email_falha():
    with patch("services.email.enviar_gmail") as mock_enviar_email:
        mock_enviar_email.return_value = False

        response = client.get("/email/enviar_email/", params={
            "email": "teste",
            "assunto": "Assunto Teste",
            "corpo": "Corpo do email"
        })

        assert response.status_code == 400
        assert response.json()["detail"] == "Não foi possível enviar o email!"
