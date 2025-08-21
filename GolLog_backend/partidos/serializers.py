from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Partido, Calificacion # Importa los modelos de la app partidos

# Serializer simple para el usuario
class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

# Serializer para el modelo Calificacion
class CalificacionSerializer(serializers.ModelSerializer):
    usuario_username = serializers.ReadOnlyField(source='usuario.username')
    partido_nombre_evento = serializers.ReadOnlyField(source='partido.nombre_evento')

    class Meta:
        model = Calificacion
        fields = [
            'id', 'usuario', 'usuario_username', 'partido', 'partido_nombre_evento', 
            'puntuacion', 'descripcion_corta', 'descripcion_larga', 'fecha_calificacion'
        ]
        read_only_fields = ['id', 'usuario', 'usuario_username', 'partido', 'partido_nombre_evento', 'fecha_calificacion']

    def create(self, validated_data):
        return Calificacion.objects.create(**validated_data)

# Serializer para el modelo Partido
class PartidoSerializer(serializers.ModelSerializer):
    equipo_local_nombre = serializers.ReadOnlyField(source='equipo_local.nombre')
    equipo_visitante_nombre = serializers.ReadOnlyField(source='equipo_visitante.nombre')
    liga_nombre = serializers.ReadOnlyField(source='liga.nombre')
    calificaciones = CalificacionSerializer(many=True, read_only=True)

    class Meta:
        model = Partido
        fields = [
            'id', 'nombre_evento', 'fecha', 'hora', 'equipo_local', 
            'equipo_visitante', 'equipo_local_nombre', 'equipo_visitante_nombre', 
            'resultado_local', 'resultado_visitante', 'liga', 'liga_nombre', 'calificaciones'
        ]
        read_only_fields = ('equipo_local_nombre', 'equipo_visitante_nombre', 'liga_nombre',)
