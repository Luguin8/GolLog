from django.db import models
from django.contrib.auth.models import User # Usaremos el modelo de usuario de Django

class Liga(models.Model):
    # Campos de TheSportsDB para Liga
    thesportsdb_id = models.CharField(max_length=50, unique=True, db_index=True)
    nombre = models.CharField(max_length=200)
    pais = models.CharField(max_length=100)
    deporte = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} ({self.pais})"

class Equipo(models.Model):
    # Campos de TheSportsDB para Equipo
    thesportsdb_id = models.CharField(max_length=50, unique=True, db_index=True)
    nombre = models.CharField(max_length=200)
    logo_url = models.URLField(max_length=500, blank=True, null=True)
    logo_imagen = models.ImageField(upload_to='logos/', blank=True, null=True)
    liga = models.ForeignKey(Liga, on_delete=models.CASCADE, related_name='equipos_de_liga')

    def __str__(self):
        return self.nombre

