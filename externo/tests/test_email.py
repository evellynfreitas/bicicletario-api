from unittest.mock import patch, MagicMock
from services.email import enviar_gmail

# Caso de sucesso
@patch("services.email.yagmail.SMTP")  # mocka o SMTP
def test_enviar_gmail_sucesso(mock_smtp):
    mock_instance = MagicMock()
    mock_smtp.return_value = mock_instance

    resultado = enviar_gmail(
        destinatario="teste@email.com",
        assunto="Assunto de Teste",
        mensagem="Mensagem teste"
    )

    assert resultado is True
    mock_instance.send.assert_called_once_with(
        to="teste@email.com",
        subject="Assunto de Teste",
        contents="Mensagem teste"
    )

# Caso de erro
@patch("services.email.yagmail.SMTP", side_effect=Exception("Falha ao enviar"))
def test_enviar_gmail_falha(mock_smtp):
    resultado = enviar_gmail(
        destinatario="teste@email.com",
        assunto="Assunto de Teste",
        mensagem="Mensagem teste"
    )

    assert resultado is False
