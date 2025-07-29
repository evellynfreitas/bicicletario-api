import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from services.tranca  import cadastrar_tranca, editar_tranca, retorna_tranca, deleta_tranca, solicitar_reparo


class MockTranca:
    def __init__(self, modelo=None, ano_fabricacao=None, localizacao=None, numero=None):
        self.modelo = modelo
        self.ano_fabricacao = ano_fabricacao
        self.localizacao = localizacao
        self.numero = numero or 1
        self.status = "NOVA"
        self.bicicleta_numero = None
        self.id_totem = None

# Mock do DB
class MockDBSession:
    def __init__(self):
        self.trancas = {}

    def add(self, obj):
        self.trancas[obj.numero] = obj

    def commit(self): pass

    def refresh(self, obj): pass

    def delete(self, obj):
        del self.trancas[obj.numero]

    def query(self, model):
        self.model = model
        return self

    def filter(self, condition):
        self.numero = condition.right.value
        return self

    def first(self):
        return self.trancas.get(self.numero)

    def all(self):
        return list(self.trancas.values())

# Mock da request
class MockRequest:
    def __init__(self, modelo="ModeloX", ano_fabricacao=2020, localizacao="Estação A", numero=None):
        self.modelo = modelo
        self.ano_fabricacao = ano_fabricacao
        self.localizacao = localizacao
        self.numero = numero or 1

@pytest.fixture
def db():
    return MockDBSession()

@pytest.fixture
def request():
    return MockRequest()

@patch("equipamento_servico.Tranca", MockTranca)
def test_cadastrar_tranca(db, request):
    result = cadastrar_tranca(request, db)
    assert result["success"]
    assert result["detail"] == "Nova tranca cadastrada com sucesso"

@patch("equipamento_servico.Tranca", MockTranca)
def test_editar_tranca(db, request):
    cadastrar_tranca(request, db)
    nova_request = MockRequest(modelo="Atualizado", ano_fabricacao=2024, localizacao="Setor B", numero=1)
    result = editar_tranca(nova_request, db)
    assert result["success"]
    assert result["detail"] == "Tranca editada com sucesso"

@patch("equipamento_servico.Tranca", MockTranca)
def test_retornar_tranca(db, request):
    cadastrar_tranca(request, db)
    result = retorna_tranca(1, db)
    assert result["success"]
    assert "tranca" in result

@patch("equipamento_servico.Tranca", MockTranca)
def test_deletar_tranca(db, request):
    cadastrar_tranca(request, db)
    result = deleta_tranca(1, db)
    assert result["success"]
    assert result["detail"] == "Tranca removida com sucesso"

@patch("equipamento_servico.Tranca", MockTranca)
def test_solicitar_reparo(db, request):
    cadastrar_tranca(request, db)
    db.trancas[1].status = "NOVA"
    result = solicitar_reparo(1, db)
    assert result["success"]
    assert result["detail"] == "Reparo solicitado com sucesso"
