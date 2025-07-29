from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Aluguel, Ciclista
from datetime import datetime
from services.ciclista import busca_ciclista_por_id


def verifica_tranca():
    print("Tranca verificada")

def verifica_alugueis_ciclista(id_ciclista, db):
    aluguel = db.query(Aluguel).filter(Aluguel.id_ciclista == id_ciclista, Aluguel.hora_fim == None).all()
    print(aluguel)
    
    if aluguel:  # Verifica se a lista não está vazia
        return {"success": False, "detail": "Ciclista já tem um aluguel em aberto"}

    return {"success": True, "detail": "Ciclista está liberado para alugar nova bicicleta"}

def envia_email(email):
    print(f"Enviei o email de confirmação para {email}.")

def remove_bicicleta_da_tranca(id_bicicleta, id_tranca):
    print(f"Removi a bicicleta {id_bicicleta} da tranca {id_tranca}.")
    
def adiciona_bicicleta_na_tranca(id_bicicleta, id_tranca):
    print(f"Adicionei a bicicleta {id_bicicleta} na tranca {id_tranca}.")

def novo_aluguel(id_ciclista, id_bicicleta, id_tranca, db):
    ciclista = busca_ciclista_por_id(id_ciclista, db)
    if ciclista is None:
        return {"success": False, "detail": "Ciclista não encontrado"}
    
    if not ciclista.ativo:
        return {"success": False, "detail": "Ciclista não está com a conta ativada"}
    
    result = verifica_alugueis_ciclista(id_ciclista, db)
    if result['success'] == False:
        return result
    
    verifica_tranca()
    remove_bicicleta_da_tranca(id_bicicleta, id_tranca)
    
    aluguel = Aluguel(id_ciclista = id_ciclista, id_bicicleta = id_bicicleta, tranca_inicial=id_tranca)
    db.add(aluguel)
    db.commit()
    db.refresh(aluguel)
    
    envia_email(ciclista.email)
    
    return {"success": True, "detail": "Novo aluguel cadastrado com sucesso"}

def devolucao(id_bicicleta, id_tranca, db):
    print(id_bicicleta)
    aluguel = db.query(Aluguel).filter(Aluguel.id_bicicleta == id_bicicleta, Aluguel.hora_fim == None).first()
    
    if aluguel is None:
        return {"success": False, "detail": "Não encontrei um aluguel em andamento para essa bicicleta"}
    
    ciclista = busca_ciclista_por_id(aluguel.id_ciclista, db)
    if ciclista is None:
        return {"success": False, "detail": "Ciclista não encontrado"}
    
    adiciona_bicicleta_na_tranca(id_bicicleta, id_tranca)
    
    aluguel.hora_fim = datetime.today()
    
    db.add(aluguel)
    db.commit()
    db.refresh(aluguel)
    
    envia_email(aluguel.id_ciclista)
    
    return {"success": True, "detail": "Bicicleta devolvida com sucesso"}
 

def resetar_banco_de_dados():
    from models import Ciclista, CartaoDeCredito, Funcionario, Aluguel
    from database import Base, engine
    from sqlalchemy.orm import Session
    from datetime import datetime, date, timedelta

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = Session(bind=engine)

    ciclistas_dados = [
        {
            "id": 1,
            "nome": "Fulano Beltrano",
            "email": "user@example.com",
            "nacionalidade": "Brasileiro",
            "cpf": "78804034009",
            "senha": "ABC123",
            "data_nascimento": date(2021, 5, 2),
            "ativo": True,
            "data_hora_confirmacao": datetime.now(),
        },
        {
            "id": 2,
            "nome": "Fulano Beltrano",
            "email": "user2@example.com",
            "nacionalidade": "Brasileiro",
            "cpf": "43943488039",
            "senha": "ABC123",
            "data_nascimento": date(2021, 5, 2),
            "ativo": False,
            "data_hora_confirmacao": None,
        },
        {
            "id": 3,
            "nome": "Fulano Beltrano",
            "email": "user3@example.com",
            "nacionalidade": "Brasileiro",
            "cpf": "10243164084",
            "senha": "ABC123",
            "data_nascimento": date(2021, 5, 2),
            "ativo": True,
            "data_hora_confirmacao": datetime.now(),
        },
        {
            "id": 4,
            "nome": "Fulano Beltrano",
            "email": "user4@example.com",
            "nacionalidade": "Brasileiro",
            "cpf": "30880150017",
            "senha": "ABC123",
            "data_nascimento": date(2021, 5, 2),
            "ativo": True,
            "data_hora_confirmacao": datetime.now(),
        },
    ]

    for dados in ciclistas_dados:
        ciclista = Ciclista(**dados)
        session.add(ciclista)
        session.flush()

        cartao = CartaoDeCredito(
            id_ciclista=ciclista.id,
            numero_cartao="4012001037141112",
            nome_titular="Fulano Beltrano",
            validade=date(2022, 12, 1),
            cvv="132",
        )
        session.add(cartao)

    funcionario = Funcionario(
        matricula=12345,
        nome="Beltrano",
        email="employee@example.com",
        cpf="99999999999",
        funcao="Reparador",
        senha="123",
        data_nascimento=date.today().replace(year=date.today().year - 25)  # idade ~25 anos
    )

    session.add(funcionario)
    
    alugueis = [
        Aluguel(
            id_ciclista=3,
            id_bicicleta=3,
            tranca_inicial=2,
            hora_inicio=datetime.now(),
            cobranca=1.0,
        ),
        Aluguel(
            id_ciclista=4,
            id_bicicleta=5,
            tranca_inicial=4,
            hora_inicio=datetime.now() - timedelta(hours=2),
            cobranca=2.0,
        ),
        Aluguel(
            id_ciclista=3,
            id_bicicleta=1,
            tranca_inicial=1,
            hora_inicio=datetime.now() - timedelta(hours=2),
            hora_fim=datetime.now(),
            cobranca=3.0
        ),
    ]

    session.add_all(alugueis)

    session.commit()
    session.close()
    