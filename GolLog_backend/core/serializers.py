from rest_framework import serializers
from .models import Liga, Equipo, Partido, Calificacion
from django.contrib.auth.models import User

# Serializer simple para el usuario
class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CalificacionSerializer(serializers.ModelSerializer):
    usuario = UserSimpleSerializer(read_only=True)  # Muestra el usuario que hizo la calificación
    partido_nombre_evento = serializers.ReadOnlyField(source='partido.nombre_evento')  # Muestra el nombre del partido

    class Meta:
        model = Calificacion
        fields = ['__all__']  # Incluye todos los campos del modelo Calificacion
        read_only_fields = ('usuario', 'partido_nombre_evento')

    def create(self, validated_data):
        return Calificacion.objects.create(**validated_data)



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
    calificaciones = CalificacionSerializer(many=True, read_only=True)  # Incluye las calificaciones del partido

    class Meta:
        model = Partido
        fields = '__all__' # Incluye todos los campos del modelo Partido
        read_only_fields = ('equipo_local_nombre', 'equipo_visitante_nombre', 'liga_nombre',)


# Serializer para el modelo Liga
class LigaSerializer(serializers.ModelSerializer):
    # Nuevo: Incluye todos los equipos relacionados con esta liga
    equipos = EquipoSerializer(many=True, read_only=True, source='equipos_de_liga') # <-- ¡Clave para relaciones inversas!

    class Meta:
        model = Liga
        fields = '__all__'

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