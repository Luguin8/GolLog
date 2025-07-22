from django.shortcuts import render

from rest_framework import viewsets, permissions
from .models import Liga, Equipo, Partido, Calificacion
from .serializers import LigaSerializer, EquipoSerializer, PartidoSerializer, CalificacionSerializer

class LigaViewSet(viewsets.ModelViewSet):
    queryset = Liga.objects.all() # Consulta para obtener todas las ligas
    serializer_class = LigaSerializer # Serializador a usar

class EquipoViewSet(viewsets.ModelViewSet):
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer

class PartidoViewSet(viewsets.ModelViewSet):
    queryset = Partido.objects.all()
    serializer_class = PartidoSerializer
    # Opcional: puedes añadir filtros aquí, ej. para buscar partidos por liga o fecha
    # from rest_framework import filters
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['nombre_evento', 'equipo_local__nombre', 'equipo_visitante__nombre']

class CalificacionViewSet(viewsets.ModelViewSet):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Permite a no autenticados leer, a autenticados crear/modificar

    # Sobrescribir perform_create para que el usuario que califica sea el usuario logueado
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    # Opcional: Filtrar calificaciones para mostrar solo las del usuario actual o de un partido específico
    def get_queryset(self):
        queryset = super().get_queryset()
        partido_id = self.request.query_params.get('partido_id', None)
        if partido_id is not None:
            queryset = queryset.filter(partido__id=partido_id)
        return queryset