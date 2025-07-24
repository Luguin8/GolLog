import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Liga, Equipo, Partido
from datetime import datetime

class Command(BaseCommand):
    help = 'Importa datos de ligas, equipos y partidos de TheSportsDB.com'

    THESPORTSDB_BASE_URL = "https://www.thesportsdb.com/api/v1/json/"
    API_KEY = getattr(settings, 'THESPORTSDB_API_KEY', None)

    def handle(self, *args, **options):
        if not self.API_KEY:
            self.stdout.write(self.style.ERROR('Error: THESPORTSDB_API_KEY no está configurada en settings_local.py'))
            return

        self.stdout.write(self.style.SUCCESS('Iniciando importación de datos de TheSportsDB...'))

        self.import_ligas()
        self.import_equipos_para_ligas()
        self.import_proximos_partidos_para_ligas()

        self.stdout.write(self.style.SUCCESS('Importación de datos finalizada.'))

    def _make_request(self, endpoint):
        url = f"{self.THESPORTSDB_BASE_URL}{self.API_KEY}/{endpoint}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Error al hacer petición a {url}: {e}"))
            return None

    def import_ligas(self):
        self.stdout.write(self.style.HTTP_INFO('Importando ligas...'))

        LIGA_IDS_TO_IMPORT = [
            "4328",  # English Premier League
            #"4406",  # Argentina Primera División
        ]

        for league_id in LIGA_IDS_TO_IMPORT:
            data = self._make_request(f"lookupleague.php?id={league_id}")
            if data and data.get('leagues'):
                league_data = data['leagues'][0]
                if league_data.get('strSport') == 'Soccer':
                    liga, created = Liga.objects.update_or_create(
                        thesportsdb_id=league_data['idLeague'],
                        defaults={
                            'nombre': league_data['strLeague'],
                            'pais': league_data['strCountry'],
                            'deporte': league_data['strSport']
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"  Liga '{liga.nombre}' creada."))
                    else:
                        self.stdout.write(self.style.MIGRATE_HEADING(f"  Liga '{liga.nombre}' actualizada."))
                else:
                    self.stdout.write(self.style.WARNING(f"  Liga ID {league_id} ('{league_data.get('strLeague', 'N/A')}') no es de fútbol. Omitiendo."))
            else:
                self.stdout.write(self.style.WARNING(f"  No se encontraron datos para la liga ID {league_id}."))

    def import_equipos_para_ligas(self):
        self.stdout.write(self.style.HTTP_INFO('Importando todos los equipos de las ligas...'))
        ligas = Liga.objects.all()
        for liga in ligas:
            self.stdout.write(self.style.NOTICE(f"  Importando equipos para la liga: {liga.nombre}"))
            data = self._make_request(f"lookup_all_teams.php?id={liga.thesportsdb_id}")
            if data and data.get('teams'):
                for team_data in data['teams']:
                    equipo, created = Equipo.objects.update_or_create(
                        thesportsdb_id=team_data['idTeam'],
                        defaults={
                            'nombre': team_data['strTeam'],
                            'logo_url': team_data.get('strTeamBadge'),
                            'liga': liga
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"    Equipo '{equipo.nombre}' creado."))
                    else:
                        self.stdout.write(self.style.MIGRATE_HEADING(f"    Equipo '{equipo.nombre}' actualizado."))
            else:
                self.stdout.write(self.style.WARNING(f"  No se encontraron equipos para la liga {liga.nombre}."))

    def import_partidos_para_ligas(self):
        self.stdout.write(self.style.HTTP_INFO('Importando partidos para ligas existentes...'))
        ligas = Liga.objects.all() # Obtiene todas las ligas
        for liga in ligas:
            self.stdout.write(self.style.NOTICE(f"  Buscando partidos futuros para la liga: {liga.nombre}"))
            # Endpoint para los próximos 15 eventos (partidos) de una liga por ID
            # eventsnextleague.php?id={idLeague}
            data = self._make_request(f"eventsnextleague.php?id={liga.thesportsdb_id}")

            if data and data.get('events'):
                for event_data in data['events']:
                    # TheSportsDB devuelve equipo local y visitante por nombre, necesitamos sus IDs de Django
                    # Busca el equipo local y visitante en tu DB de Django
                    equipo_local_obj = Equipo.objects.filter(
                        nombre=event_data['strHomeTeam'],
                        liga=liga # Asegura que sea de la liga correcta
                    ).first()
                    equipo_visitante_obj = Equipo.objects.filter(
                        nombre=event_data['strAwayTeam'],
                        liga=liga # Asegura que sea de la liga correcta
                    ).first()

                    if not equipo_local_obj or not equipo_visitante_obj:
                        self.stdout.write(self.style.WARNING(
                            f"    Saltando partido (equipos no encontrados): {event_data.get('strEvent')} "
                            f"Local: {event_data['strHomeTeam']} Visitante: {event_data['strAwayTeam']}"))
                        continue # Si no encontramos los equipos en nuestra DB, saltamos este partido

                    # Convertir fechas y horas
                    event_date = None
                    if event_data.get('dateEvent'):
                        try:
                            event_date = datetime.datetime.strptime(event_data['dateEvent'], '%Y-%m-%d').date()
                        except ValueError:
                            self.stdout.write(self.style.WARNING(f"    Fecha de evento inválida para {event_data.get('strEvent')}: {event_data.get('dateEvent')}"))

                    event_time = None
                    if event_data.get('strTime'):
                        try:
                            event_time = datetime.datetime.strptime(event_data['strTime'], '%H:%M:%S').time()
                        except ValueError:
                            # A veces strTime es solo HH:MM
                            try:
                                event_time = datetime.datetime.strptime(event_data['strTime'], '%H:%M').time()
                            except ValueError:
                                self.stdout.write(self.style.WARNING(f"    Hora de evento inválida para {event_data.get('strEvent')}: {event_data.get('strTime')}"))


                    if event_date: # Solo procesamos si tenemos una fecha válida
                        partido, created = Partido.objects.update_or_create(
                            thesportsdb_id=event_data['idEvent'],
                            defaults={
                                'liga': liga,
                                'equipo_local': equipo_local_obj,
                                'equipo_visitante': equipo_visitante_obj,
                                'fecha': event_date,
                                'hora': event_time,
                                'resultado_local': event_data.get('intHomeScore') if event_data.get('intHomeScore') else None,
                                'resultado_visitante': event_data.get('intAwayScore') if event_data.get('intAwayScore') else None,
                                'estado': event_data.get('strStatus', 'Programado') # Usar 'strStatus' si existe, sino 'Programado'
                            }
                        )
                        if created:
                            self.stdout.write(self.style.SUCCESS(f"      Partido '{partido.equipo_local.nombre} vs {partido.equipo_visitante.nombre}' creado."))
                        else:
                            self.stdout.write(self.style.MIGRATE_HEADING(f"      Partido '{partido.equipo_local.nombre} vs {partido.equipo_visitante.nombre}' actualizado."))
            else:
                self.stdout.write(self.style.WARNING(f"  No se encontraron partidos futuros para la liga {liga.nombre}."))

# --- Modifica el método handle para llamar a la nueva función ---
    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP_INFO('Iniciando importación de datos de TheSportsDB...'))
        self.import_ligas()
        self.import_equipos_para_ligas()
        # ¡Añade la llamada a la nueva función aquí!
        self.import_partidos_para_ligas()
        self.stdout.write(self.style.SUCCESS('Importación de datos completada.'))