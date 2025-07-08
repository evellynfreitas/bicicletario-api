from util import EMAIL_USER, EMAIL_PASSWORD

def enviar_gmail(destinatario, assunto, mensagem):
    try:
        import yagmail
        print(EMAIL_PASSWORD, EMAIL_USER)

        yag = yagmail.SMTP(user=EMAIL_USER, password=EMAIL_PASSWORD)

        yag.send(
            to=destinatario,
            subject=assunto,
            contents=mensagem
        )
        return True
    
    except Exception as ex:
        print(ex)
        return False
