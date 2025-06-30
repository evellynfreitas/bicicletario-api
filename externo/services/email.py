import smtplib
from email.mime.text import MIMEText
from util import EMAIL_USER, EMAIL_PASSWORD

def enviar_gmail(destinatario, assunto, mensagem):
    try:
        print(EMAIL_PASSWORD)
        import yagmail

        yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASSWORD)

        yag.send(
            to=destinatario,
            subject=assunto,
            contents=mensagem
        )
        return True
    
    except Exception as ex:
        print(ex)
        return False
