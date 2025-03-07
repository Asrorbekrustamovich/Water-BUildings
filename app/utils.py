from django.core.mail import send_mail
from django.conf import settings
import smtplib
import dns.resolver
from email.message import EmailMessage

import dns.resolver
import smtplib

def email_exists(email):
    domain = email.split('@')[-1]

    try:
        # MX rekordlarni olish
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_record = str(mx_records[0].exchange).rstrip('.')

        # SMTP serverga bog‘lanib tekshirish
        try:
            server = smtplib.SMTP(mx_record, timeout=5)
            server.quit()
            return True  # ✅ Email domeni mavjud
        except (smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected):
            return False  # ❌ Email domeni SMTP orqali tekshirib bo‘lmadi

    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return False  # ❌ Domen mavjud emas yoki noto‘g‘ri



def send_email_to_users(viloyat, company, phonenumber, ism, familiya, email, xabar):
    """Emailni jo‘natishdan oldin mavjudligini tekshirish"""
    if not email_exists(email):
        print(f"Email mavjud emas: {email}")
        return False  # Email topilmadi

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
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True  # EMAIL MUVAFFAQIYATLI JO‘NATILDI
    except smtplib.SMTPException as e:
        print(f"Email jo'natishda xatolik: {e}")
        return False  # XATOLIK CHIQDI
