from django.db import models
from django.contrib.auth.models import User
from core.models import Liga, Equipo # Importa los modelos de la app core

class Partido(models.Model):
    # Campos de TheSportsDB para Evento/Partido
    thesportsdb_id = models.CharField(max_length=50, unique=True, db_index=True)
    equipo_local_tsdb_id = models.CharField(max_length=50)
    equipo_visitante_tsdb_id = models.CharField(max_length=50)
    equipo_local = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='partidos_local')
    equipo_visitante = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='partidos_visitante')
    nombre_evento = models.CharField(max_length=255)
    fecha = models.DateField()
    hora = models.TimeField()
    liga = models.ForeignKey(Liga, on_delete=models.CASCADE, related_name='partidos')
    temporada = models.CharField(max_length=50)
    resultado_local = models.IntegerField(null=True, blank=True)
    resultado_visitante = models.IntegerField(null=True, blank=True)
    estadio = models.CharField(max_length=200, blank=True, null=True)
    status_partido = models.CharField(max_length=50, default='Programado')

    def __str__(self):
        return f"{self.equipo_local.nombre} vs {self.equipo_visitante.nombre} - {self.fecha} ({self.liga.nombre})"

    class Meta:
        ordering = ['-fecha', '-hora']

class Calificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calificaciones')
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE, related_name='calificaciones')
    puntuacion = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    descripcion_larga = models.TextField(blank=True, null=True)
    descripcion_corta = models.CharField(max_length=30, blank=True, null=True)
    fecha_calificacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'partido')
        ordering = ['-fecha_calificacion']

    def __str__(self):
        return f"Calificación de {self.usuario.username} ({self.puntuacion}) para {self.partido.nombre_evento}"

