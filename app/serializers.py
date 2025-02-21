from rest_framework import serializers
from .models import Role, User, viloyat, MCHJ, Xodimlar, MCHJUser, Holat, Instrument,Type

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
        model = viloyat
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