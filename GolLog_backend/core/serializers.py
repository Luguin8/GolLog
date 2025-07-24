from rest_framework import serializers
from .models import Liga, Equipo, Partido, Calificacion
from django.contrib.auth.models import User

# Serializer para el modelo Liga
class LigaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liga
        fields = '__all__' # Incluye todos los campos del modelo Liga

# Serializer para el modelo Equipo
class EquipoSerializer(serializers.ModelSerializer):
    liga_nombre = serializers.ReadOnlyField(source='liga.nombre') # Muestra el nombre de la liga en lugar del ID

    class Meta:
        model = Equipo
        fields = '__all__' # Incluye todos los campos del modelo Equipo
        read_only_fields = ('liga_nombre',) # Hace que este campo sea de solo lectura

# Serializer para el modelo Partido
class PartidoSerializer(serializers.ModelSerializer):
    equipo_local_nombre = serializers.ReadOnlyField(source='equipo_local.nombre')
    equipo_visitante_nombre = serializers.ReadOnlyField(source='equipo_visitante.nombre')
    liga_nombre = serializers.ReadOnlyField(source='liga.nombre')

    class Meta:
        model = Partido
        fields = '__all__' # Incluye todos los campos del modelo Partido
        read_only_fields = ('equipo_local_nombre', 'equipo_visitante_nombre', 'liga_nombre',)

# Serializer para el modelo User (solo campos públicos o necesarios para calificaciones)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username'] # Solo incluye el ID y el nombre de usuario

# Serializer para el modelo Calificacion
class CalificacionSerializer(serializers.ModelSerializer):
    usuario_username = serializers.ReadOnlyField(source='usuario.username') # Muestra el nombre de usuario
    partido_nombre_evento = serializers.ReadOnlyField(source='partido.nombre_evento') # Muestra el nombre del partido

    class Meta:
        model = Calificacion
        fields = '__all__' # Incluye todos los campos del modelo Calificacion
        read_only_fields = ('usuario_username', 'partido_nombre_evento',)