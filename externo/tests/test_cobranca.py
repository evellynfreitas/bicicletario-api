import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from unittest.mock import MagicMock, patch
from services.cobranca import cadastrar_cobranca, editar_cobranca, retorna_cobranca, lista_cobrancas, processa_cobrancas


# Mock de request para criação
class CobrancaRequest:
    def __init__(self, ciclista, valor):
        self.ciclista = ciclista
        self.valor = valor


def test_cadastrar_cobranca_sucesso():
    request = CobrancaRequest("ciclista_123", 50.0)
    db = MagicMock()

    resultado = cadastrar_cobranca(request, db)

    assert resultado["success"] is True
    assert resultado["detail"] == "Nova cobrança cadastrada com sucesso"
    db.add.assert_called()
    db.commit.assert_called()
    db.refresh.assert_called()


def test_cadastrar_cobranca_falha():
    request = CobrancaRequest("ciclista_123", 50.0)
    db = MagicMock()
    db.add.side_effect = Exception("Erro")

    resultado = cadastrar_cobranca(request, db)

    assert resultado["success"] is False
    assert resultado["detail"] == "Não foi possível cadastrar a cobrança"


def test_editar_cobranca_sucesso():
    db = MagicMock()
    cobranca_mock = MagicMock()
    db.query().filter().first.return_value = cobranca_mock

    resultado = editar_cobranca(1, "PAGA", db)

    assert resultado["success"] is True
    assert resultado["detail"] == "Cobrança editada com sucesso"
    assert cobranca_mock.status == "PAGA"


def test_editar_cobranca_nao_encontrada():
    db = MagicMock()
    db.query().filter().first.return_value = None

    resultado = editar_cobranca(1, "PAGA", db)

    assert resultado["success"] is False
    assert resultado["detail"] == "Cobrança não encontrada com esse ID"


def test_editar_cobranca_status_invalido():
    db = MagicMock()
    cobranca_mock = MagicMock()
    db.query().filter().first.return_value = cobranca_mock

    resultado = editar_cobranca(1, "INVALIDO", db)

    assert resultado["success"] is False
    assert resultado["detail"] == "Status de cobrança não reconhecido"


def test_retorna_cobranca_sucesso():
    db = MagicMock()
    db.query().filter().first.return_value = "CobrancaTeste"
    resultado = retorna_cobranca(1, db)
    assert resultado == "CobrancaTeste"


def test_retorna_cobranca_falha():
    db = MagicMock()
    db.query().filter().first.return_value = None
    resultado = retorna_cobranca(1, db)
    assert resultado["success"] is False
    assert resultado["detail"] == "Cobrança não encontrada com esse ID"


def test_lista_cobrancas_com_resultado():
    db = MagicMock()
    db.query().all.return_value = ["Cobranca1", "Cobranca2"]
    resultado = lista_cobrancas(db)
    assert resultado == ["Cobranca1", "Cobranca2"]


def test_lista_cobrancas_vazia():
    db = MagicMock()
    db.query().all.return_value = None
    resultado = lista_cobrancas(db)
    assert resultado["success"] is False
    assert resultado["detail"] == "Não foi encontrada nenhuma cobrança"


@patch("services.cobranca.enviar_gmail", return_value=True)
def test_processa_cobrancas_sucesso(mock_email):
    db = MagicMock()
    cobranca_mock = MagicMock()
    cobranca_mock.valor = 50.0
    cobranca_mock.status = "PENDENTE"
    cobranca_mock.hora_solicitacao = "2025-07-07 10:00:00"

    db.query().filter().all.return_value = [cobranca_mock]

    resultado = processa_cobrancas(db)

    assert resultado["success"] is True
    assert resultado["detail"] == "Cobranças realizadas com sucesso"
    mock_email.assert_called_once()


@patch("services.cobranca.enviar_gmail", return_value=False)
def test_processa_cobrancas_falha_envio(mock_email):
    db = MagicMock()
    cobranca_mock = MagicMock()
    cobranca_mock.valor = 50.0
    cobranca_mock.status = "PENDENTE"
    cobranca_mock.hora_solicitacao = "2025-07-07 10:00:00"

    db.query().filter().all.return_value = [cobranca_mock]

    resultado = processa_cobrancas(db)

    assert resultado["success"] is False
    assert resultado["detail"] == "Não foi possível enviar o email"
