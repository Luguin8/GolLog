from rest_framework import serializers
from .models import Perfil
from django.contrib.auth.models import User
from core.models import Equipo

class PerfilSerializer(serializers.ModelSerializer):
    usuario = serializers.ReadOnlyField(source='usuario.username')
    equipo_favorito_nombre = serializers.ReadOnlyField(source='equipo_favorito.nombre')

    class Meta:
        model = Perfil
        fields = ['id', 'usuario', 'foto_perfil', 'descripcion_corta', 'equipo_favorito', 'equipo_favorito_nombre', 'pais']
        read_only_fields = ['id', 'usuario', 'equipo_favorito_nombre']

class UserProfileSerializer(serializers.ModelSerializer):
    perfil = PerfilSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'perfil']
        read_only_fields = ['id', 'username', 'first_name', 'last_name']
