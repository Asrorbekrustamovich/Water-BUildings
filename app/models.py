from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

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
    class Meta:
        db_table = 'users'

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

#notification kerak
#dockument saqlash model uchun kerak
# class Type(models.Model):
#     type_name = models.CharField(max_length=255)

#     class Meta:
#         db_table = 'type'

#     def __str__(self):
#         return self.type_name



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
