from rest_framework import viewsets, permissions, generics
from rest_framework import filters as drf_filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Liga, Equipo
from .serializers import LigaSerializer, EquipoSerializer, RegisterSerializer
from django.contrib.auth.models import User

class LigaViewSet(viewsets.ModelViewSet):
    queryset = Liga.objects.all().prefetch_related('equipos_de_liga')
    serializer_class = LigaSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre', 'pais', 'deporte']

class EquipoViewSet(viewsets.ModelViewSet):
    queryset = Equipo.objects.all().select_related('liga')
    serializer_class = EquipoSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter]
    filterset_fields = ['nombre', 'liga__nombre', 'liga']
    search_fields = ['nombre', 'liga__nombre']

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
