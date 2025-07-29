import pytest
from unittest.mock import patch
from services.email import enviar_gmail
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Cobranca
from services.cobranca import cadastrar_cobranca, editar_cobranca, retorna_cobranca, lista_cobrancas, processa_cobrancas
from unittest.mock import patch

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_cadastrar_cobranca_sucesso(db_session):
    class Request:
        ciclista = 123
        valor = 45.50

    result = cadastrar_cobranca(Request, db_session)

    assert result["success"] is True
    cobrancas = db_session.query(Cobranca).all()
    assert len(cobrancas) == 1
    assert cobrancas[0].status == "PENDENTE"


def test_editar_cobranca_status(db_session):
    cobranca = Cobranca(ciclista=1, valor=20.0, status="PENDENTE")
    db_session.add(cobranca)
    db_session.commit()

    result = editar_cobranca(cobranca.id, "PAGA", db_session)

    assert result["success"] is True
    atualizada = db_session.query(Cobranca).filter_by(id=cobranca.id).first()
    assert atualizada.status == "PAGA"


def test_retornar_cobranca_existente(db_session):
    cobranca = Cobranca(ciclista=42, valor=99.9, status="PENDENTE")
    db_session.add(cobranca)
    db_session.commit()

    retorno = retorna_cobranca(cobranca.id, db_session)
    assert retorno.id == cobranca.id


def test_lista_cobrancas(db_session):
    db_session.add_all([
        Cobranca(ciclista=1, valor=10.0, status="PENDENTE"),
        Cobranca(ciclista=2, valor=15.0, status="PAGA")
    ])
    db_session.commit()

    resultado = lista_cobrancas(db_session)
    assert len(resultado) == 2

@patch("services.cobranca.requests.get")
@patch("services.cobranca.enviar_gmail")
def test_processa_cobrancas_sucesso(mock_email, mock_get, db_session):
    cobranca = Cobranca(ciclista=99, valor=70.0, status="PENDENTE", hora_solicitacao=datetime.now())
    db_session.add(cobranca)
    db_session.commit()

    # mock da API externa
    mock_get.return_value.ok = True
    mock_get.return_value.json.return_value = {"email": "ciclista@test.com"}
    mock_email.return_value = True

    resultado = processa_cobrancas(db_session)

    assert resultado["success"] is True
    cobranca_final = db_session.query(Cobranca).first()
    assert cobranca_final.status == "PAGA"
    assert cobranca_final.hora_finalizacao is not None


# Teste de integração com mock para yagmail
@patch("services.email.yagmail.SMTP.send")
@patch("services.email.yagmail.SMTP")
def test_enviar_gmail_sucesso(mock_smtp_class, mock_send):

    mock_smtp_instance = mock_smtp_class.return_value
    mock_send.return_value = None

    destinatario = "teste@email.com"
    assunto = "Assunto Teste"
    mensagem = "Mensagem de teste"

    resultado = enviar_gmail(destinatario, assunto, mensagem)
    assert resultado is True

    mock_smtp_class.assert_called_once()
    mock_smtp_instance.send.assert_called_once_with(
        to=destinatario,
        subject=assunto,
        contents=mensagem
    )
