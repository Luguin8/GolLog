from django.shortcuts import render

from rest_framework import viewsets, permissions, generics
from rest_framework import filters as drf_filters
from django_filters.rest_framework import DjangoFilterBackend # Mantén esta importación si la usas en otro ViewSet
from .models import Liga, Equipo, Partido, Calificacion
from .serializers import LigaSerializer, EquipoSerializer, PartidoSerializer, CalificacionSerializer, RegisterSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .permissions import IsOwnerOrReadOnly   # Importa tu permiso personalizado si lo necesitas
from django.contrib.auth.models import User

class LigaViewSet(viewsets.ModelViewSet):
    queryset = Liga.objects.all().prefetch_related('equipos_de_liga')
    serializer_class = LigaSerializer
    permission_classes = [permissions.AllowAny] # Permite acceso a cualquiera para leer ligas
    filter_backends = [DjangoFilterBackend] # Habilita el filtrado
    filterset_fields = ['nombre', 'pais', 'deporte'] # Campos por los que se puede filtrar

class EquipoViewSet(viewsets.ModelViewSet):
    queryset = Equipo.objects.all().select_related('liga')
    serializer_class = EquipoSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter]
    filterset_fields = ['nombre', 'liga__nombre', 'liga'] # Filtrar por nombre de equipo, nombre de liga o ID de liga
    search_fields = ['nombre', 'liga__nombre']  # Permite búsqueda por nombre de equipo o nombre de liga

class PartidoViewSet(viewsets.ModelViewSet):
    queryset = Partido.objects.all().select_related('liga', 'equipo_local', 'equipo_visitante').prefetch_related('calificaciones')
    serializer_class = PartidoSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter] 
    filterset_fields = ['liga__nombre', 'equipo_local__nombre', 'equipo_visitante__nombre', 'fecha', 'status_partido']
    search_fields = ['nombre_evento', 'equipo_local__nombre', 'equipo_visitante__nombre']
    ordering_fields = ['fecha', 'hora', 'nombre_evento']  # Permite ordenar por estos campos

class CalificacionViewSet(viewsets.ModelViewSet):
    queryset = Calificacion.objects.all().select_related('usuario', 'partido')
    serializer_class = CalificacionSerializer
    # Para las calificaciones, podrías querer que solo usuarios autenticados puedan crearlas,
    # y que solo el propietario o un admin pueda actualizarlas/eliminarlas.
    # Por ahora, permitimos solo lectura para no complicar la autenticación todavía.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]  # Permite a cualquier usuario leer, pero solo al propietario editar/eliminar.
                                             # Para producción, deberías usar IsAuthenticatedOrReadOnly
                                             # o IsAuthenticated y permisos personalizados.
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['usuario__username', 'partido__nombre_evento', 'puntuacion']

    # Sobrescribe perform_create para asignar el usuario actual automáticamente
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        partido_id = self.request.query_params.get('partido_id', None)
        if partido_id is not None:
            queryset = queryset.filter(partido__id=partido_id)
        return queryset
    
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer