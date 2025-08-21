from rest_framework import serializers
from .models import Liga, Equipo
from django.contrib.auth.models import User


# Serializer simple para el usuario
class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

# Serializer para el modelo Equipo
class EquipoSerializer(serializers.ModelSerializer):
    liga_nombre = serializers.ReadOnlyField(source='liga.nombre')

    class Meta:
        model = Equipo
        fields = '__all__'
        read_only_fields = ('liga_nombre',)

# Serializer para el modelo Liga
class LigaSerializer(serializers.ModelSerializer):
    equipos = EquipoSerializer(many=True, read_only=True, source='equipos_de_liga')

    class Meta:
        model = Liga
        fields = '__all__'

# Serializer para el registro de usuarios
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
