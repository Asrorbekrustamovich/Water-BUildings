from django.core.mail import send_mail
from django.conf import settings
import smtplib
from email.message import EmailMessage

def send_email_to_users(title, viloyat, company, phonenumber, ism, familiya, email, xabar):
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
    msg['Subject'] = title
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = email

    try:
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True  # EMAIL MUVAFFAQIYATLI JO‘NATILDI
    except smtplib.SMTPException as e:
        print(f"Email jo'natishda xatolik: {e}")
        return False  # XATOLIK CHIQDI

