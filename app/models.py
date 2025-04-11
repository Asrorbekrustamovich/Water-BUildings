from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone
class Role(models.Model):
    name=models.CharField(max_length=255)
    def __str__(self):
        return self.name

class User(models.Model):
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    user_name_or_full_name=models.CharField(max_length=255)
    role=models.ForeignKey(Role,on_delete=models.CASCADE)#direktor, mchj, admin
    phone=models.CharField(max_length=255,null=True,blank=True)
    adress=models.CharField(max_length=255,null=True,blank=True)
    company=models.CharField(max_length=255,null=True,blank=True)
    founded_year=models.CharField(max_length=255,null=True,blank=True)
    STR=models.CharField(max_length=255,null=True,blank=True)
    Licence=models.CharField(max_length=255,null=True,blank=True)
    Tashkiliy_Huquq_shakli=models.CharField(max_length=255,blank=True,null=True)
    position=models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
        return self.login

class viloyat(models.Model):
    name = models.CharField(max_length=255)
    class Meta:
        db_table = 'viloyat'

    def __str__(self):
        return self.name

class MCHJ(models.Model):
    name = models.CharField(max_length=255)
    viloyat = models.ForeignKey(viloyat, on_delete=models.CASCADE) 
    class Meta:
        db_table = 'mchj'

    def __str__(self):
        return self.name
class Xodimlar(models.Model):
    full_name = models.CharField(max_length=255)
    mchj=models.ForeignKey(MCHJ, on_delete=models.CASCADE)
    phone=models.CharField(max_length=255)


class MCHJUser(models.Model):
    mchj = models.ForeignKey(MCHJ,null=True ,on_delete=models.CASCADE)
    user = models.ForeignKey(User,  null=True ,on_delete=models.CASCADE)

    class Meta:
        db_table = 'mchj_user'

    def __str__(self):
        return self.mchj.name+' - '+self.user.user_name_or_full_name    



class Type(models.Model):    
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Holat(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'holat'

    def __str__(self):
        return self.name

class Instrument(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    texnika_turi = models.CharField(max_length=255)
    rusumi = models.CharField(max_length=255, default='kiritilmagan', null=True, blank=True)
    zavod_raqami = models.CharField(max_length=255, default='kiritilmagan', null=True, blank=True)
    davlat_raqami = models.CharField(max_length=255, default='kiritilmagan', null=True, blank=True)
    sana = models.CharField(max_length=255, null=True, blank=True)
    texnik_holati = models.ForeignKey(Holat, on_delete=models.CASCADE)
    soni = models.IntegerField(default=0, null=True, blank=True)
    mchj = models.ForeignKey(MCHJ, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'instrument'

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

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"
class Notification(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notification'

    def __str__(self):
        return f"Notification for message {self.message.id} - Read: {self.is_read}"
class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')
    original_name = models.CharField(max_length=255, editable=True)
    custom_name = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.id:
            self.original_name = self.file.name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.custom_name if self.custom_name else self.original_name

    class Meta:
        db_table = 'document'