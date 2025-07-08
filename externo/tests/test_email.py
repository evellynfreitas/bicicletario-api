import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from unittest.mock import patch, MagicMock
from util import EMAIL_USER, EMAIL_PASSWORD
from services.email import enviar_gmail


@patch("services.email.yagmail.SMTP")
def test_enviar_gmail_sucesso(mock_smtp):
    mock_yag = MagicMock()
    mock_smtp.return_value = mock_yag

    resultado = enviar_gmail("destino@email.com", "Assunto Teste", "Mensagem Teste")

    assert resultado is True
    mock_smtp.assert_called_once_with(user=EMAIL_USER, password=EMAIL_PASSWORD)
    mock_yag.send.assert_called_once_with(
        to="destino@email.com",
        subject="Assunto Teste",
        contents="Mensagem Teste"
    )


@patch("services.email.yagmail.SMTP", side_effect=Exception("Erro no SMTP"))
def test_enviar_gmail_falha(mock_smtp):
    resultado = enviar_gmail("destino@email.com", "Assunto Teste", "Mensagem Teste")
    assert resultado is False
