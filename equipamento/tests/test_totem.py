from unittest.mock import MagicMock
from services.totem import cadastrar_totem, editar_totem, retorna_totem, lista_totens, deleta_totem, TOTEM_NAO_ENCONTRADO

class TotemRequest:
    def __init__(self, numero=None, localizacao=None, descricao=None):
        self.numero = numero
        self.localizacao = localizacao
        self.descricao = descricao

def test_cadastrar_totem_sucesso():
    request = TotemRequest(localizacao="Praça Central", descricao="Totem novo")
    db = MagicMock()

    resultado = cadastrar_totem(request, db)

    assert resultado["success"] is True
    assert resultado["detail"] == "Novo totem cadastrado com sucesso"
    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()

def test_cadastrar_totem_falha():
    request = TotemRequest(localizacao="Praça Central", descricao="Totem novo")
    db = MagicMock()
    db.add.side_effect = Exception("Erro")

    resultado = cadastrar_totem(request, db)

    assert resultado["success"] is False
    assert resultado["detail"] == "Não foi possível cadastrar o novo totem"

def test_editar_totem_sucesso():
    db = MagicMock()
    totem_mock = MagicMock()
    db.query().filter().first.return_value = totem_mock

    request = TotemRequest(numero=1, localizacao="Novo lugar", descricao="Atualizado")

    resultado = editar_totem(request, db)

    assert resultado["success"] is True
    assert resultado["detail"] == "Totem editado com sucesso"
    assert totem_mock.localizacao == "Novo lugar"
    assert totem_mock.descricao == "Atualizado"

def test_editar_totem_nao_encontrado():
    db = MagicMock()
    db.query().filter().first.return_value = None
    request = TotemRequest(numero=1, localizacao="X", descricao="Y")

    resultado = editar_totem(request, db)

    assert resultado["success"] is False
    assert resultado["detail"] == TOTEM_NAO_ENCONTRADO

def test_retorna_totem_sucesso():
    db = MagicMock()
    totem_mock = MagicMock()
    db.query().filter().first.return_value = totem_mock

    resultado = retorna_totem(123, db)

    assert resultado["success"] is True
    assert resultado["totem"] == totem_mock

def test_retorna_totem_nao_encontrado():
    db = MagicMock()
    db.query().filter().first.return_value = None

    resultado = retorna_totem(999, db)

    assert resultado["success"] is False
    assert resultado["detail"] == TOTEM_NAO_ENCONTRADO

def test_lista_totens():
    db = MagicMock()
    db.query().all.return_value = ["Totem1", "Totem2"]

    resultado = lista_totens(db)

    assert resultado == ["Totem1", "Totem2"]

def test_deleta_totem_sucesso():
    db = MagicMock()
    totem_mock = MagicMock()
    db.query().filter().first.return_value = totem_mock

    resultado = deleta_totem(1, db)

    assert resultado["success"] is True
    assert resultado["detail"] == "Totem removido com sucesso"
    db.delete.assert_called_once_with(totem_mock)
    db.commit.assert_called_once()

def test_deleta_totem_nao_encontrado():
    db = MagicMock()
    db.query().filter().first.return_value = None

    resultado = deleta_totem(1, db)

    assert resultado["success"] is False
    assert resultado["detail"] == TOTEM_NAO_ENCONTRADO
