from django.core.mail import send_mail
from django.conf import settings
import smtplib
from email.message import EmailMessage
from app.models import *
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

from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    # Add custom claims to access token
    refresh['user_id'] = user.id
    refresh['role_id'] = user.role.id if user.role else None

    if user.id == 1 :
        refresh['mchj_id'] = 0
    else:
        mchj_user = MCHJUser.objects.filter(user=user).first()
        refresh['mchj_id'] = mchj_user.mchj.id if mchj_user else None

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

