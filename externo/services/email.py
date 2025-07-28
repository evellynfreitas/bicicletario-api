from util import EMAIL_USER, EMAIL_PASSWORD
import yagmail

def enviar_gmail(destinatario, assunto, mensagem):
    try:

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
