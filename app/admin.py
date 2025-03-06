from django.contrib import admin
from .models import User, Role, MCHJ, Xodimlar, Viloyat, MCHJUser, Type, Holat, Instrument, Message, Notification, Document

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("login", "user_name_or_full_name", "role", "phone", "address", "is_staff", "is_superuser")
    search_fields = ("login", "user_name_or_full_name", "phone")
    list_filter = ("role", "is_staff", "is_superuser")

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(MCHJ)
class MCHJAdmin(admin.ModelAdmin):
    list_display = ("name", "viloyat")
    search_fields = ("name",)
    list_filter = ("viloyat",)

@admin.register(Xodimlar)
class XodimlarAdmin(admin.ModelAdmin):
    list_display = ("full_name", "mchj", "phone")
    search_fields = ("full_name", "phone")

@admin.register(Viloyat)
class ViloyatAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(MCHJUser)
class MCHJUserAdmin(admin.ModelAdmin):
    list_display = ("mchj", "user")
    search_fields = ("mchj__name", "user__login")

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Holat)
class HolatAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ("texnika_turi", "rusumi", "zavod_raqami", "davlat_raqami", "texnik_holati", "soni", "mchj")
    search_fields = ("texnika_turi", "rusumi", "zavod_raqami", "davlat_raqami")
    list_filter = ("texnik_holati", "mchj")

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "timestamp", "is_read")
    search_fields = ("sender__login", "receiver__login", "content")
    list_filter = ("is_read",)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("message", "is_read", "timestamp")
    search_fields = ("message__content",)
    list_filter = ("is_read",)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("user", "original_name", "custom_name", "uploaded_at")
    search_fields = ("original_name", "custom_name")
    list_filter = ("uploaded_at",)
