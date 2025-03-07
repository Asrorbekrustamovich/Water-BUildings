from django.core.mail import send_mail
from django.conf import settings
import smtplib
import dns.resolver
from email.message import EmailMessage

def email_exists(email):
    """SMTP orqali email manzilining mavjudligini tekshirish"""
    domain = email.split('@')[-1]  # Email domenini ajratib olish

    try:
        # 1. MX yozuvlarini olish
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_record = str(mx_records[0].exchange)

        # 2. SMTP serverga bog‘lanish
        server = smtplib.SMTP(mx_record)
        server.set_debuglevel(0)
        server.helo()
        server.mail('test@example.com')  # Soxta jo‘natuvchi manzili
        code, message = server.rcpt(email)
        server.quit()

        # 3. Agar kod 250 bo‘lsa, email mavjud
        return code == 250
    except Exception:
        return False

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
