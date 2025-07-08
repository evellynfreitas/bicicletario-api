import pytest
from datetime import date, timedelta
from services.cartao import valida_cartao

# Mock de entrada simulando a estrutura do cartão
class CartaoMock:
    def __init__(self, numero_cartao, validade, cvv):
        self.numero_cartao = numero_cartao
        self.validade = validade
        self.cvv = cvv

# Sucesso
def test_valida_cartao_sucesso():
    cartao = CartaoMock(
        numero_cartao="1234567890123456",
        validade=date.today() + timedelta(days=30),
        cvv="123"
    )
    response = valida_cartao(cartao)
    assert response["success"] is True
    assert response["detail"] == "Cartão validado com a administradora"

# Número inválido (não dígito)
def test_valida_cartao_numero_invalido_nao_digito():
    cartao = CartaoMock("1234abcd567", date.today() + timedelta(days=30), "123")
    response = valida_cartao(cartao)
    assert response["success"] is False
    assert response["detail"] == "O número do cartão é inválido"

# Número inválido (muito curto)
def test_valida_cartao_numero_curto():
    cartao = CartaoMock("1234567", date.today() + timedelta(days=30), "123")
    response = valida_cartao(cartao)
    assert response["success"] is False
    assert response["detail"] == "O número do cartão é inválido"

# Número inválido (muito longo)
def test_valida_cartao_numero_longo():
    cartao = CartaoMock("1" * 20, date.today() + timedelta(days=30), "123")
    response = valida_cartao(cartao)
    assert response["success"] is False
    assert response["detail"] == "O número do cartão é inválido"

# Cartão expirado
def test_valida_cartao_expirado():
    cartao = CartaoMock("1234567890123", date.today() - timedelta(days=1), "123")
    response = valida_cartao(cartao)
    assert response["success"] is False
    assert response["detail"] == "Cartão expirado"

# CVV inválido (tamanho errado)
def test_valida_cartao_cvv_tamanho_errado():
    cartao = CartaoMock("1234567890123", date.today() + timedelta(days=30), "12")
    response = valida_cartao(cartao)
    assert response["success"] is False
    assert response["detail"] == "CVV inválido"

# CVV inválido (não numérico)
def test_valida_cartao_cvv_invalido_nao_digito():
    cartao = CartaoMock("1234567890123", date.today() + timedelta(days=30), "1a3")
    response = valida_cartao(cartao)
    assert response["success"] is False
    assert response["detail"] == "CVV inválido"
