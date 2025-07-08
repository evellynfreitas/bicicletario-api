from unittest.mock import MagicMock, patch
from services.bicicleta import cadastrar_bicicleta, editar_bicicleta, retorna_bicicleta, lista_bicicletas, deleta_bicicleta, solicita_reparo_bicicleta


# Mock para request
class BicicletaRequest:
    def __init__(self, numero=None, marca=None, modelo=None, ano=None):
        self.numero = numero
        self.marca = marca
        self.modelo = modelo
        self.ano = ano

def test_cadastrar_bicicleta_sucesso():
    db = MagicMock()
    request = BicicletaRequest(marca="Caloi", modelo="Elite", ano=2020)

    resultado = cadastrar_bicicleta(request, db)

    assert resultado["success"] is True
    assert resultado["detail"] == "Nova bicicleta cadastrada com sucesso"
    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()

def test_cadastrar_bicicleta_falha():
    db = MagicMock()
    db.add.side_effect = Exception("Erro")
    request = BicicletaRequest(marca="Caloi", modelo="Elite", ano=2020)

    resultado = cadastrar_bicicleta(request, db)

    assert resultado["success"] is False
    assert resultado["detail"] == "Não foi possível cadastrar a nova bicicleta"

def test_editar_bicicleta_sucesso():
    db = MagicMock()
    bicicleta_mock = MagicMock()
    db.query().filter().first.return_value = bicicleta_mock

    request = BicicletaRequest(numero=1, marca="NovaMarca", modelo="NovoModelo", ano=2024)

    resultado = editar_bicicleta(request, db)

    assert resultado["success"] is True
    assert bicicleta_mock.marca == "NovaMarca"
    assert bicicleta_mock.modelo == "NovoModelo"
    assert bicicleta_mock.ano == 2024

def test_editar_bicicleta_nao_encontrada():
    db = MagicMock()
    db.query().filter().first.return_value = None
    request = BicicletaRequest(numero=1, marca="X", modelo="Y", ano=2022)

    resultado = editar_bicicleta(request, db)

    assert resultado["success"] is False
    assert resultado["detail"] == "Bicicleta não encontrada"

def test_retorna_bicicleta_sucesso():
    db = MagicMock()
    bicicleta_mock = MagicMock()
    db.query().filter().first.return_value = bicicleta_mock

    resultado = retorna_bicicleta(123, db)

    assert resultado["success"] is True
    assert resultado["bicicleta"] == bicicleta_mock

def test_retorna_bicicleta_nao_encontrada():
    db = MagicMock()
    db.query().filter().first.return_value = None

    resultado = retorna_bicicleta(999, db)

    assert resultado["success"] is False
    assert resultado["detail"] == "Bicicleta não encontrado"

def test_lista_bicicletas():
    db = MagicMock()
    db.query().all.return_value = ["Bike1", "Bike2"]

    resultado = lista_bicicletas(db)

    assert resultado == ["Bike1", "Bike2"]

def test_deleta_bicicleta_sucesso():
    db = MagicMock()
    bicicleta_mock = MagicMock()
    db.query().filter().first.return_value = bicicleta_mock

    resultado = deleta_bicicleta(1, db)

    assert resultado["success"] is True
    db.delete.assert_called_once_with(bicicleta_mock)
    db.commit.assert_called_once()

def test_deleta_bicicleta_nao_encontrada():
    db = MagicMock()
    db.query().filter().first.return_value = None

    resultado = deleta_bicicleta(1, db)

    assert resultado["success"] is False
    assert resultado["detail"] == "Bicicleta não encontrada"

@patch("services.bicicleta.retorna_bicicleta")
def test_solicita_reparo_bicicleta(mock_retorna_bicicleta):
    db = MagicMock()
    bicicleta_mock = MagicMock()
    mock_retorna_bicicleta.return_value = {"bicicleta": bicicleta_mock}

    resultado = solicita_reparo_bicicleta(1, db)

    assert resultado["success"] is True
    assert resultado["detail"] == "Reparo solicitado com sucesso"
    assert bicicleta_mock.status == "REPARO SOLICITADO"
    db.add.assert_called_once_with(bicicleta_mock)
    db.commit.assert_called_once()
