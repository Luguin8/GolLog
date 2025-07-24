from django.db import models
from django.contrib.auth.models import User # Usaremos el modelo de usuario de Django

class Liga(models.Model):
    # Campos de TheSportsDB para Liga
    thesportsdb_id = models.CharField(max_length=50, unique=True, db_index=True) # ID único de la liga en TheSportsDB
    nombre = models.CharField(max_length=200) # strLeague
    pais = models.CharField(max_length=100)   # strCountry
    deporte = models.CharField(max_length=100) # strSport (debería ser 'Soccer')
    # Puedes añadir otros campos de la API si los necesitas, ej. strBadge (logo de la liga)

    def __str__(self):
        return f"{self.nombre} ({self.pais})"

class Equipo(models.Model):
    # Campos de TheSportsDB para Equipo
    thesportsdb_id = models.CharField(max_length=50, unique=True, db_index=True) # ID único del equipo en TheSportsDB
    nombre = models.CharField(max_length=200) # strTeam
    logo_url = models.URLField(max_length=500, blank=True, null=True) # strTeamBadge (URL del logo)
    liga = models.ForeignKey(Liga, on_delete=models.CASCADE, related_name='equipos') # Equipo pertenece a una Liga

    def __str__(self):
        return self.nombre

class Partido(models.Model):
    # Campos de TheSportsDB para Evento/Partido
    thesportsdb_id = models.CharField(max_length=50, unique=True, db_index=True) # ID único del evento en TheSportsDB (idEvent)
    equipo_local_tsdb_id = models.CharField(max_length=50) # idHomeTeam de TheSportsDB (lo guardamos para referencia al importar)
    equipo_visitante_tsdb_id = models.CharField(max_length=50) # idAwayTeam de TheSportsDB (lo guardamos para referencia al importar)
    equipo_local = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='partidos_local')
    equipo_visitante = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='partidos_visitante')
    nombre_evento = models.CharField(max_length=255) # strEvent o combinación de equipos
    fecha = models.DateField()       # dateEvent
    hora = models.TimeField()        # strTime
    liga = models.ForeignKey(Liga, on_delete=models.CASCADE, related_name='partidos')
    temporada = models.CharField(max_length=50) # strSeason, ej. '2023-2024'
    resultado_local = models.IntegerField(null=True, blank=True) # intHomeScore
    resultado_visitante = models.IntegerField(null=True, blank=True) # intAwayScore
    estadio = models.CharField(max_length=200, blank=True, null=True) # strVenue
    status_partido = models.CharField(max_length=50, default='Programado')
    # Puedes añadir más campos como strStatus (si el partido ha terminado o no), etc.

    def __str__(self):
        return f"{self.equipo_local.nombre} vs {self.equipo_visitante.nombre} - {self.fecha} ({self.liga.nombre})"

    class Meta:
        ordering = ['-fecha', '-hora'] # Ordenar partidos por fecha descendente por defecto

class Calificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calificaciones')
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE, related_name='calificaciones')
    puntuacion = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)]) # Del 1 al 5
    comentario = models.TextField(blank=True, null=True)
    fecha_calificacion = models.DateTimeField(auto_now_add=True) # Guarda la fecha y hora de la calificación automáticamente

    class Meta:
        # Asegura que un usuario solo pueda calificar un partido una vez
        unique_together = ('usuario', 'partido')
        ordering = ['-fecha_calificacion'] # Ordenar calificaciones por fecha descendente

    def __str__(self):
        return f"Calificación de {self.usuario.username} ({self.puntuacion}) para {self.partido.nombre_evento}"