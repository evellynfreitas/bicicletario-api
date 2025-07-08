from unittest.mock import MagicMock, patch
from services.tranca import cadastrar_tranca, editar_tranca, retorna_tranca, lista_trancas, deleta_tranca, incluir_tranca_totem, novo_reparo, inserir_bicicleta_tranca, remover_bicicleta, solicitar_reparo


def test_cadastrar_tranca_sucesso():
    db = MagicMock()
    request = MagicMock(modelo="Modelo A", ano_fabricacao=2022, localizacao="Local A")
    result = cadastrar_tranca(request, db)
    assert result["success"]
    db.add.assert_called_once()
    db.commit.assert_called_once()

def test_cadastrar_tranca_falha():
    db = MagicMock()
    db.add.side_effect = Exception("Erro")
    request = MagicMock()
    result = cadastrar_tranca(request, db)
    assert not result["success"]

def test_editar_tranca_sucesso():
    db = MagicMock()
    tranca_mock = MagicMock()
    db.query().filter().first.return_value = tranca_mock
    request = MagicMock(numero=1, modelo="Novo Modelo", ano_fabricacao=2020, localizacao="Nova Local")
    result = editar_tranca(request, db)
    assert result["success"]
    assert tranca_mock.modelo == "Novo Modelo"

def test_editar_tranca_nao_encontrada():
    db = MagicMock()
    db.query().filter().first.return_value = None
    request = MagicMock(numero=99)
    result = editar_tranca(request, db)
    assert not result["success"]

def test_retorna_tranca_sucesso():
    db = MagicMock()
    tranca_mock = MagicMock()
    db.query().filter().first.return_value = tranca_mock
    result = retorna_tranca(1, db)
    assert result["success"]
    assert result["tranca"] == tranca_mock

def test_retorna_tranca_erro():
    db = MagicMock()
    db.query().filter().first.return_value = None
    result = retorna_tranca(1, db)
    assert not result["success"]

def test_lista_trancas():
    db = MagicMock()
    db.query().all.return_value = [1, 2, 3]
    result = lista_trancas(db)
    assert result == [1, 2, 3]

def test_deleta_tranca_sucesso():
    db = MagicMock()
    tranca = MagicMock()
    db.query().filter().first.return_value = tranca
    result = deleta_tranca(1, db)
    assert result["success"]
    db.delete.assert_called_once_with(tranca)

def test_deleta_tranca_erro():
    db = MagicMock()
    db.query().filter().first.return_value = None
    result = deleta_tranca(1, db)
    assert not result["success"]

@patch("services.tranca.enviar_email")
def test_incluir_tranca_totem(mock_email):
    db = MagicMock()
    tranca = MagicMock(status="NOVA")
    db.query().filter().first.return_value = tranca
    result = incluir_tranca_totem(1, 123, 321, db)
    assert result["success"]
    assert tranca.status == "DISPONIVEL"
    assert tranca.id_totem == 321

@patch("services.tranca.enviar_email")
def test_novo_reparo(mock_email):
    db = MagicMock()
    tranca = MagicMock(status="REPARO SOLICITADO", bicicleta_numero=None)
    db.query().filter().first.return_value = tranca
    result = novo_reparo(1, 10, db)
    assert result["detail"] == "A tranca foi removida para reparo"
    assert tranca.status == "EM REPARO"

@patch("services.tranca.enviar_email")
def test_inserir_bicicleta_tranca(mock_email):
    db = MagicMock()

    bicicleta = MagicMock(status="NOVA")
    tranca = MagicMock(status="DISPONIVEL", id_totem=99)

    # Mock para bicicleta
    bicicleta_query = MagicMock()
    bicicleta_query.filter.return_value.first.return_value = bicicleta
    # Mock para tranca
    tranca_query = MagicMock()
    tranca_query.filter.return_value.first.return_value = tranca

    db.query.side_effect = [bicicleta_query, tranca_query]
    
    result = inserir_bicicleta_tranca(1, 2, 10, db)
    assert result["success"]
    assert bicicleta.status == "DISPONIVEL"
    assert tranca.bicicleta_numero == 1

@patch("services.tranca.enviar_email")
def test_remover_bicicleta_reparo(mock_email):
    db = MagicMock()
    tranca = MagicMock(bicicleta_numero=123)
    bicicleta = MagicMock(numero=123, status="REPARO SOLICITADO")

    tranca_query = MagicMock()
    tranca_query.filter.return_value.first.return_value = tranca

    bicicleta_query = MagicMock()
    bicicleta_query.filter.return_value.first.return_value = bicicleta

    db.query.side_effect = [tranca_query, bicicleta_query]

    result = remover_bicicleta(1, 10, "REPARO", db)
    assert result["success"]
    assert bicicleta.status == "EM REPARO"
    assert bicicleta.localizacao == "Oficina"

@patch("services.tranca.retorna_tranca")
def test_solicitar_reparo(mock_retorna):
    db = MagicMock()
    tranca = MagicMock()
    mock_retorna.return_value = {"tranca": tranca}
    result = solicitar_reparo(1, db)
    assert result["success"]
    assert tranca.status == "REPARO SOLICITADO"
    db.commit.assert_called_once()
