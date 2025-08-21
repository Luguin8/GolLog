from rest_framework import viewsets, permissions, filters as drf_filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Partido, Calificacion
from .serializers import PartidoSerializer, CalificacionSerializer
from core.permissions import IsOwnerOrReadOnly # Asume que el archivo de permisos está en core/permissions.py
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response

class PartidoViewSet(viewsets.ModelViewSet):
    queryset = Partido.objects.all().select_related('liga', 'equipo_local', 'equipo_visitante').prefetch_related('calificaciones')
    serializer_class = PartidoSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter] 
    filterset_fields = ['liga__nombre', 'equipo_local__nombre', 'equipo_visitante__nombre', 'fecha', 'status_partido']
    search_fields = ['nombre_evento', 'equipo_local__nombre', 'equipo_visitante__nombre']
    ordering_fields = ['fecha', 'hora', 'nombre_evento']

class CalificacionViewSet(viewsets.ModelViewSet):
    queryset = Calificacion.objects.all().select_related('usuario', 'partido')
    serializer_class = CalificacionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['usuario__username', 'partido__nombre_evento', 'puntuacion']

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        partido_id = self.request.query_params.get('partido_id', None)
        if partido_id is not None:
            queryset = queryset.filter(partido__id=partido_id)
        return queryset

class PartidoRecienteViewSet(viewsets.ReadOnlyModelViewSet):
    # Devuelve los 5 partidos más recientes que ya tienen resultado
    queryset = Partido.objects.filter(resultado_local__isnull=False, resultado_visitante__isnull=False).order_by('-fecha', '-hora')[:5]
    serializer_class = PartidoSerializer
    permission_classes = [permissions.AllowAny]
