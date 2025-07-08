import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from services.aluguel import novo_aluguel, devolucao
from models import Aluguel, Ciclista


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def mock_ciclista():
    ciclista = MagicMock(spec=Ciclista)
    ciclista.id = 1
    ciclista.ativo = True
    ciclista.email = "teste@teste.com"
    return ciclista


def test_novo_aluguel_sucesso(mock_db, mock_ciclista):
    mock_db.query().filter().all.return_value = []

    with patch("services.aluguel.busca_ciclista_por_id", return_value=mock_ciclista), \
         patch("services.aluguel.verifica_tranca"), \
         patch("services.aluguel.remove_bicicleta_da_tranca"), \
         patch("services.aluguel.envia_email"):

        response = novo_aluguel(1, 1, 1, mock_db)
        assert response["success"] is True
        assert response["detail"] == "Novo aluguel cadastrado com sucesso"


def test_novo_aluguel_ciclista_inexistente(mock_db):
    with patch("services.aluguel.busca_ciclista_por_id", return_value=None):
        response = novo_aluguel(1, 1, 1, mock_db)
        assert response["success"] is False
        assert response["detail"] == "Ciclista não encontrado"


def test_novo_aluguel_ciclista_inativo(mock_db, mock_ciclista):
    mock_ciclista.ativo = False
    with patch("services.aluguel.busca_ciclista_por_id", return_value=mock_ciclista):
        response = novo_aluguel(1, 1, 1, mock_db)
        assert response["success"] is False
        assert response["detail"] == "Ciclista não está com a conta ativada"


def test_novo_aluguel_ja_tem_em_aberto(mock_db, mock_ciclista):
    mock_db.query().filter().all.return_value = [MagicMock()]

    with patch("services.aluguel.busca_ciclista_por_id", return_value=mock_ciclista):
        response = novo_aluguel(1, 1, 1, mock_db)
        assert response["success"] is False
        assert response["detail"] == "Ciclista já tem um aluguel em aberto"


def test_devolucao_sucesso(mock_db, mock_ciclista):
    aluguel_mock = MagicMock(spec=Aluguel)
    aluguel_mock.id_ciclista = 1

    mock_db.query().filter().first.return_value = aluguel_mock

    with patch("services.aluguel.busca_ciclista_por_id", return_value=mock_ciclista), \
         patch("services.aluguel.adiciona_bicicleta_na_tranca"), \
         patch("services.aluguel.envia_email"):

        response = devolucao(1, 1, mock_db)
        assert response["success"] is True
        assert response["detail"] == "Bicicleta devolvida com sucesso"


def test_devolucao_sem_aluguel(mock_db):
    mock_db.query().filter().first.return_value = None
    response = devolucao(1, 1, mock_db)
    assert response["success"] is False
    assert response["detail"] == "Não encontrei um aluguel em andamento para essa bicicleta"


def test_devolucao_ciclista_inexistente(mock_db):
    aluguel_mock = MagicMock(spec=Aluguel)
    aluguel_mock.id_ciclista = 1
    mock_db.query().filter().first.return_value = aluguel_mock

    with patch("services.aluguel.busca_ciclista_por_id", return_value=None):
        response = devolucao(1, 1, mock_db)
        assert response["success"] is False
        assert response["detail"] == "Ciclista não encontrado"
