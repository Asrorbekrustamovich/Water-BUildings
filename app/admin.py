from django.contrib import admin
from app.models import (
    Document, Role, User, Viloyat, MCHJ, Xodimlar, MCHJUser,
    Type, Holat, Instrument, Message, Notification
)

admin.site.register(Document)
admin.site.register(Role)
admin.site.register(User)
admin.site.register(Viloyat)
admin.site.register(MCHJ)
admin.site.register(Xodimlar)
admin.site.register(MCHJUser)
admin.site.register(Type)
admin.site.register(Holat)
admin.site.register(Instrument)
admin.site.register(Message)
admin.site.register(Notification)
