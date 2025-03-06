from rest_framework import serializers
from .models import Role, User, Viloyat, MCHJ, Xodimlar, MCHJUser, Holat, Instrument,Type,Message,Notification
from .models import Document
from django.contrib.auth import get_user_model
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'user', 'file', 'original_name', 'custom_name', 'uploaded_at']
        read_only_fields = ['original_name', 'uploaded_at']

    def create(self, validated_data):
        validated_data['original_name'] = validated_data['file'].name
        return super().create(validated_data)
    
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'login', 'user_name_or_full_name', 'phone', 'address', 'role', 'is_active', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  # Parol faqat yozish mumkin, qaytishda ko‘rinmaydi
        }

    def create(self, validated_data):
        """Yangi foydalanuvchi yaratishda parolni shifrlash"""
        user = User(
            login=validated_data['login'],
            user_name_or_full_name=validated_data.get('user_name_or_full_name', ''),
            phone=validated_data.get('phone', ''),
            address=validated_data.get('address', ''),
            role=validated_data.get('role', None),
        )
        user.set_password(validated_data['password'])  # Parolni shifrlash
        user.save()
        return user

    def update(self, instance, validated_data):
        """Foydalanuvchini yangilash"""
        instance.login = validated_data.get('login', instance.login)
        instance.user_name_or_full_name = validated_data.get('user_name_or_full_name', instance.user_name_or_full_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.address = validated_data.get('address', instance.address)
        instance.role = validated_data.get('role', instance.role)
        instance.is_active = validated_data.get('is_active', instance.is_active)

        # Agar parol o‘zgartirilgan bo‘lsa, shifrlab saqlash
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        instance.save()
        return instance
    
class ViloyatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Viloyat
        fields = '__all__'

class MCHJSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCHJ
        fields = '__all__'

class XodimlarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Xodimlar
        fields = '__all__'

class MCHJUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCHJUser
        fields = '__all__'

class TypeSerializer(serializers.ModelSerializer):
     class Meta:
         model = Type
         fields = '__all__'

class HolatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Holat
        fields = '__all__'

class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = '__all__'
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
from rest_framework import serializers
from .models import User, MCHJUser, MCHJ

class MCHJUserSerializer(serializers.ModelSerializer):
    mchj_name = serializers.CharField(source='mchj.name', read_only=True)
    user_name_or_full_name = serializers.CharField(source='user.user_name_or_full_name', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)
    address = serializers.CharField(source='mchj.address', read_only=True)
    viloyat = serializers.CharField(source='mchj.viloyat.name', read_only=True)

    class Meta:
        model = MCHJUser
        fields = ['mchj_name', 'user_name_or_full_name', 'phone', 'address', 'viloyat']
