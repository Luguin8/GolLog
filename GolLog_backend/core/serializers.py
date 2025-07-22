from rest_framework import serializers
from .models import Liga, Equipo, Partido, Calificacion
from django.contrib.auth.models import User # Necesario para serializar el usuario en Calificacion

class LigaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liga
        fields = '__all__' # Incluye todos los campos del modelo Liga

class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = '__all__' # Incluye todos los campos del modelo Equipo

class PartidoSerializer(serializers.ModelSerializer):
    # Para mostrar los nombres de los equipos y la liga directamente en el JSON
    equipo_local_nombre = serializers.ReadOnlyField(source='equipo_local.nombre')
    equipo_visitante_nombre = serializers.ReadOnlyField(source='equipo_visitante.nombre')
    liga_nombre = serializers.ReadOnlyField(source='liga.nombre')

    class Meta:
        model = Partido
        fields = [
            'id', # ID interno de Django
            'thesportsdb_id',
            'equipo_local', 'equipo_local_nombre',
            'equipo_visitante', 'equipo_visitante_nombre',
            'nombre_evento', 'fecha', 'hora',
            'liga', 'liga_nombre',
            'temporada', 'resultado_local', 'resultado_visitante', 'estadio'
        ]
        # Si quisieras solo ver los IDs de los equipos y la liga, usarías:
        # fields = '__all__'
        # Pero para el frontend, tener los nombres es más útil.

class CalificacionSerializer(serializers.ModelSerializer):
    # Para mostrar el nombre de usuario y el nombre del partido directamente
    usuario_username = serializers.ReadOnlyField(source='usuario.username')
    partido_nombre = serializers.ReadOnlyField(source='partido.nombre_evento')

    class Meta:
        model = Calificacion
        fields = [
            'id',
            'usuario', 'usuario_username',
            'partido', 'partido_nombre',
            'puntuacion', 'comentario', 'fecha_calificacion'
        ]