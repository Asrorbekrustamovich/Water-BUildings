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
        fields = '__all__'
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
    class Meta:
        model = MCHJUser
        fields = "__all__"
