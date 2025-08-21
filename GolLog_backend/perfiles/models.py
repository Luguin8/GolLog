from django.db import models
from django.contrib.auth.models import User
from core.models import Equipo

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    foto_perfil = models.ImageField(upload_to='perfiles/', null=True, blank=True)
    descripcion_corta = models.CharField(max_length=30, null=True, blank=True) # Corregido a 30 caracteres
    equipo_favorito = models.ForeignKey(Equipo, on_delete=models.SET_NULL, null=True, blank=True)
    pais = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'Perfil de {self.usuario.username}'

