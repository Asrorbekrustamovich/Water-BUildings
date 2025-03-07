from django.core.mail import send_mail
from django.conf import settings
import smtplib
from email.message import EmailMessage

def send_email_to_users(viloyat, company, phonenumber, ism, familiya, email, xabar):
    """Emailni jo‘natish funksiyasi"""

    body = f"""
    Viloyat: {viloyat}
    Kompaniya: {company}
    Telefon raqami: {phonenumber}
    Ism: {ism}
    Familiya: {familiya}
    Email: {email}
    Xabar: {xabar}
    """

    msg = EmailMessage()
    msg.set_content(body)
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = "asrorrustamovich007@gmail.com"

    try:
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=10)
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.send_message(msg)
        server.quit()
        return "Email muvaffaqiyatli jo'natildi"
    except smtplib.SMTPException as e:
        return f"Email jo'natishda xatolik: {e}"
    except OSError as e:
        return f"Tarmoq muammosi: {e}"  # Agar ulanish umuman bo‘lmasa
