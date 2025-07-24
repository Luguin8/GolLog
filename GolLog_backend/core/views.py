from django.shortcuts import render

from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend # Mantén esta importación si la usas en otro ViewSet
from .models import Liga, Equipo, Partido, Calificacion
from .serializers import LigaSerializer, EquipoSerializer, PartidoSerializer, CalificacionSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

class LigaViewSet(viewsets.ModelViewSet):
    queryset = Liga.objects.all()
    serializer_class = LigaSerializer
    permission_classes = [permissions.AllowAny] # Permite acceso a cualquiera para leer ligas
    filter_backends = [DjangoFilterBackend] # Habilita el filtrado
    filterset_fields = ['nombre', 'pais', 'deporte'] # Campos por los que se puede filtrar
class EquipoViewSet(viewsets.ModelViewSet):
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre', 'liga__nombre', 'liga'] # Filtrar por nombre de equipo, nombre de liga o ID de liga

class PartidoViewSet(viewsets.ModelViewSet):
    queryset = Partido.objects.all()
    serializer_class = PartidoSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['liga__nombre', 'equipo_local__nombre', 'equipo_visitante__nombre', 'fecha', 'status_partido']

class CalificacionViewSet(viewsets.ModelViewSet):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer
    # Para las calificaciones, podrías querer que solo usuarios autenticados puedan crearlas,
    # y que solo el propietario o un admin pueda actualizarlas/eliminarlas.
    # Por ahora, permitimos solo lectura para no complicar la autenticación todavía.
    permission_classes = [permissions.AllowAny] # Esto es solo para desarrollo.
                                             # Para producción, deberías usar IsAuthenticatedOrReadOnly
                                             # o IsAuthenticated y permisos personalizados.
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['usuario__username', 'partido__nombre_evento', 'puntuacion']

    # Sobrescribe perform_create para asignar el usuario actual automáticamente
    def perform_create(self, serializer):
        # Asume que el usuario está autenticado. Si usas AllowAny, esto podría fallar
        # si intentas crear una calificación sin autenticarte.
        if self.request.user.is_authenticated:
            serializer.save(usuario=self.request.user)
        else:
            # Manejar el caso donde no hay usuario autenticado (por ejemplo, elevar una excepción)
            # O permitir usuarios anónimos si tu lógica de negocio lo permite (no recomendado para calificaciones)
            raise serializer.ValidationError("Se requiere autenticación para crear una calificación.")

class CalificacionViewSet(viewsets.ModelViewSet):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        partido_id = self.request.query_params.get('partido_id', None)
        if partido_id is not None:
            queryset = queryset.filter(partido__id=partido_id)
        return queryset