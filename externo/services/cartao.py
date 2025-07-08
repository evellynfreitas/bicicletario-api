from datetime import date

def valida_cartao(cartao):
    if not cartao.numero_cartao.isdigit() or len(cartao.numero_cartao) < 13 or len(cartao.numero_cartao) > 19:
        return {"success": False, "detail": "O número do cartão é inválido"}

    if cartao.validade < date.today():
        return {"success": False, "detail": "Cartão expirado"}

    if len(cartao.cvv) != 3 or not cartao.cvv.isdigit():
        return {"success": False, "detail": "CVV inválido"}

    return {"success": True, "detail": "Cartão validado com a administradora"}

