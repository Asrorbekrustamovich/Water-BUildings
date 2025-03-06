from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, login, password=None, **extra_fields):
        """Oddiy foydalanuvchi yaratish"""
        if not login:
            raise ValueError("The Login field must be set")
        
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password=None, **extra_fields):
        """Superuser yaratish"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(login, password, **extra_fields)

class Role(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name

class User(AbstractUser):
    username = None  # AbstractUser dagi username maydonini olib tashlaymiz
    login = models.CharField(max_length=255, unique=True)  # login asosiy identifikator bo‘ladi
    user_name_or_full_name = models.CharField(max_length=255, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)  # Role bo‘lishi shart emas
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    objects = UserManager()  # Custom user manager

    USERNAME_FIELD = "login"  # Django autentifikatsiya uchun loginni ishlatadi
    REQUIRED_FIELDS = []  # Endi boshqa maydonlar majburiy emas

    class Meta:
        db_table = "users"
        ordering = ["-id"]

    def __str__(self):
        return self.login


class Viloyat(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'viloyat'
        ordering = ['-id']  # id bo'yicha teskari tartibda saralash

    def __str__(self):
        return self.name

class MCHJ(models.Model):
    name = models.CharField(max_length=255)
    viloyat = models.ForeignKey(Viloyat, on_delete=models.CASCADE)

    class Meta:
        db_table = 'mchj'
        ordering = ['-id']  # id bo'yicha teskari tartibda saralash

    def __str__(self):
        return self.name

class Xodimlar(models.Model):
    full_name = models.CharField(max_length=255)
    mchj = models.ForeignKey(MCHJ, on_delete=models.CASCADE)
    phone = models.TextField()

    class Meta:
        ordering = ['-id']  # id bo'yicha teskari tartibda saralash

    def __str__(self):
        return self.full_name

class MCHJUser(models.Model):
    mchj = models.ForeignKey(MCHJ, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'mchj_user'
        ordering = ['-id']  # id bo'yicha teskari tartibda saralash

    def __str__(self):
        return f"{self.mchj.name} - {self.user.user_name_or_full_name}"

class Type(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['-id']  # id bo'yicha teskari tartibda saralash

    def __str__(self):
        return self.name

class Holat(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'holat'
        ordering = ['-id']  # id bo'yicha teskari tartibda saralash

    def __str__(self):
        return self.name

class Instrument(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    texnika_turi = models.CharField(max_length=255)
    rusumi = models.CharField(max_length=255, default='kiritilmagan', null=True, blank=True)
    zavod_raqami = models.CharField(max_length=255, default='kiritilmagan', null=True, blank=True)
    davlat_raqami = models.CharField(max_length=255, default='kiritilmagan', null=True, blank=True)
    sana = models.DateField(null=True, blank=True)
    texnik_holati = models.ForeignKey(Holat, on_delete=models.CASCADE)
    soni = models.IntegerField(default=0, null=True, blank=True)
    mchj = models.ForeignKey(MCHJ, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'instrument'
        ordering = ['-id']  # id bo'yicha teskari tartibda saralash

    def __str__(self):
        return self.texnika_turi

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = 'message'
        ordering = ['-id']  # id bo'yicha teskari tartibda saralash

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"

class Notification(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notification'
        ordering = ['-id']  # id bo'yicha teskari tartibda saralash

    def __str__(self):
        return f"Notification for message {self.message.id} - Read: {self.is_read}"

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')
    original_name = models.CharField(max_length=255, editable=True)
    custom_name = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'document'
        ordering = ['-id']  # id bo'yicha teskari tartibda saralash

    def save(self, *args, **kwargs):
        if not self.id:
            self.original_name = self.file.name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.custom_name if self.custom_name else self.original_name