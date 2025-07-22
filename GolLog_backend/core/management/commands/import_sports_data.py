import requests
from django.core.management.base import BaseCommand
from django.conf import settings # Para acceder a THESPORTSDB_API_KEY
from core.models import Liga, Equipo, Partido
from datetime import datetime

class Command(BaseCommand):
    help = 'Importa datos de ligas, equipos y partidos de TheSportsDB.com'

    THESPORTSDB_BASE_URL = "https://www.thesportsdb.com/api/v1/json/"
    API_KEY = getattr(settings, 'THESPORTSDB_API_KEY', None) # Obtiene la API Key de settings_local.py

    def handle(self, *args, **options):
        if not self.API_KEY:
            self.stdout.write(self.style.ERROR('Error: THESPORTSDB_API_KEY no está configurada en settings_local.py'))
            self.stdout.write(self.style.ERROR('Asegurate de crear GolLog_backend/GolLog_backend/settings_local.py y agregar THESPORTSDB_API_KEY = "TU_API_KEY_AQUI"'))
            return

        self.stdout.write(self.style.SUCCESS('Iniciando importación de datos de TheSportsDB...'))

        # --- 1. Importar Ligas ---
        self.import_ligas()

        # --- 2. Importar Equipos para las Ligas existentes ---
        self.import_equipos_para_ligas()

        # --- 3. Importar Partidos (ej. los próximos de las ligas principales) ---
        self.import_proximos_partidos_para_ligas()

        self.stdout.write(self.style.SUCCESS('Importación de datos finalizada.'))

    def _make_request(self, endpoint):
        """Helper para hacer peticiones HTTP a TheSportsDB."""
        url = f"{self.THESPORTSDB_BASE_URL}{self.API_KEY}/{endpoint}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Lanza un error para códigos de estado HTTP 4xx/5xx
            return response.json()
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Error al hacer petición a {url}: {e}"))
            return None

    def import_ligas(self):
        self.stdout.write(self.style.HTTP_INFO('Importando ligas...'))
        
        # Lista de IDs de ligas populares de fútbol que TheSportsDB soporta.
        # Puedes encontrar más en su API o en su sitio web.
        LIGA_IDS_TO_IMPORT = [
            "4335", # La Liga (España)
            "4328", # Premier League (Inglaterra)
            "4396", # Serie A (Italia)
            "4334", # Ligue 1 (Francia)
            "4331", # Bundesliga (Alemania)
            "4356", # Argentinian Primera Division (Argentina)
            "4337", # Brazilian Serie A (Brasil)
            "4346", # Major League Soccer (USA)
            # Agrega más IDs de ligas si te interesan otras
        ]
        
        for league_id in LIGA_IDS_TO_IMPORT:
            data = self._make_request(f"lookupleague.php?id={league_id}")
            if data and data.get('leagues'):
                league_data = data['leagues'][0]
                if league_data.get('strSport') == 'Soccer': # Asegurarse de que sea fútbol
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
        self.stdout.write(self.style.HTTP_INFO('Importando equipos para ligas existentes...'))
        ligas = Liga.objects.all() # Obtiene todas las ligas que ya guardamos
        for liga in ligas:
            self.stdout.write(self.style.NOTICE(f"  Buscando equipos para la liga: {liga.nombre}"))
            # Endpoint para todos los equipos de una liga por ID
            data = self._make_request(f"lookup_all_teams.php?id={liga.thesportsdb_id}")
            if data and data.get('teams'):
                for team_data in data['teams']:
                    equipo, created = Equipo.objects.update_or_create(
                        thesportsdb_id=team_data['idTeam'],
                        defaults={
                            'nombre': team_data['strTeam'],
                            'logo_url': team_data.get('strTeamBadge'), # strTeamBadge puede ser nulo o no existir
                            'liga': liga
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"    Equipo '{equipo.nombre}' creado."))
                    else:
                        self.stdout.write(self.style.MIGRATE_HEADING(f"    Equipo '{equipo.nombre}' actualizado."))
            else:
                self.stdout.write(self.style.WARNING(f"  No se encontraron equipos para la liga {liga.nombre}."))

    def import_proximos_partidos_para_ligas(self):
        self.stdout.write(self.style.HTTP_INFO('Importando próximos partidos para ligas existentes...'))
        ligas = Liga.objects.all() # Obtiene todas las ligas que ya guardamos
        for liga in ligas:
            self.stdout.write(self.style.NOTICE(f"  Buscando próximos partidos para la liga: {liga.nombre}"))
            # Endpoint para los próximos 100 eventos (partidos) de una liga por su ID
            data = self._make_request(f"eventsnextleague.php?id={liga.thesportsdb_id}")
            if data and data.get('events'):
                for event_data in data['events']:
                    # Intentar encontrar los objetos Equipo existentes
                    try:
                        equipo_local = Equipo.objects.get(thesportsdb_id=event_data['idHomeTeam'])
                        equipo_visitante = Equipo.objects.get(thesportsdb_id=event_data['idAwayTeam'])
                    except Equipo.DoesNotExist:
                        self.stdout.write(self.style.WARNING(
                            f"    Saltando partido {event_data.get('strEvent', 'N/A')} - Equipo no encontrado en la DB (IDs: {event_data.get('idHomeTeam', 'N/A')}, {event_data.get('idAwayTeam', 'N/A')})."
                        ))
                        continue # Saltar este partido si los equipos no están en nuestra DB

                    # Convertir fecha y hora de string a objetos datetime
                    try:
                        fecha_obj = datetime.strptime(event_data['dateEvent'], '%Y-%m-%d').date()
                        hora_str = event_data.get('strTime', '00:00:00') # Usar 00:00:00 si no hay hora
                        hora_obj = datetime.strptime(hora_str, '%H:%M:%S').time()
                    except ValueError as e:
                        self.stdout.write(self.style.ERROR(
                            f"    Error de formato de fecha/hora para {event_data.get('strEvent', 'N/A')}: {e}. Omitiendo."
                        ))
                        continue

                    # Asegurarse de que los resultados sean enteros o None
                    home_score = int(event_data['intHomeScore']) if event_data.get('intHomeScore') else None
                    away_score = int(event_data['intAwayScore']) if event_data.get('intAwayScore') else None

                    partido, created = Partido.objects.update_or_create(
                        thesportsdb_id=event_data['idEvent'],
                        defaults={
                            'equipo_local_tsdb_id': event_data['idHomeTeam'],
                            'equipo_visitante_tsdb_id': event_data['idAwayTeam'],
                            'equipo_local': equipo_local,
                            'equipo_visitante': equipo_visitante,
                            'nombre_evento': event_data.get('strEvent', f"{equipo_local.nombre} vs {equipo_visitante.nombre}"),
                            'fecha': fecha_obj,
                            'hora': hora_obj,
                            'liga': liga,
                            'temporada': event_data.get('strSeason'),
                            'resultado_local': home_score,
                            'resultado_visitante': away_score,
                            'estadio': event_data.get('strVenue')
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"    Partido '{partido.nombre_evento}' creado."))
                    else:
                        self.stdout.write(self.style.MIGRATE_HEADING(f"    Partido '{partido.nombre_evento}' actualizado."))
            else:
                self.stdout.write(self.style.WARNING(f"  No se encontraron próximos partidos para la liga {liga.nombre}."))