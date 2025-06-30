import smtplib
from email.mime.text import MIMEText
from util import EMAIL_USER, EMAIL_PASSWORD

def enviar_gmail(destinatario, assunto, mensagem):
    try:
        import yagmail

        yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASSWORD)

        yag.send(
            to=destinatario,
            subject=assunto,
            contents=mensagem
        )
        return True
    
    except Exception as ex:
        return False

def enviar_email2(destinatario, assunto, mensagem):
    
    try:
        remetente = "bicicletario@bikes.br"
        msg = MIMEText(mensagem)
        msg['Subject'] = assunto
        msg['From'] = remetente
        msg['To'] = destinatario

        smtp_server = "sandbox.smtp.mailtrap.io"
        smtp_port = 587
        smtp_username = "78bf376501adfa"
        smtp_password = "cc39f31a6d8faf"

        with smtplib.SMTP(smtp_server, smtp_port) as servidor:
            servidor.starttls()
            servidor.login(smtp_username, smtp_password)
            servidor.sendmail(remetente, destinatario, msg.as_string())

        return True

    except Exception:
        return False
