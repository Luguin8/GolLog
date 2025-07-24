# C:\Users\Martin\Desktop\GolLog\GolLog_backend\core\management\commands\import_sports_data.py

from django.core.management.base import BaseCommand
from django.conf import settings
import requests
from core.models import Liga, Equipo, Partido
import datetime
import json # ¡Añade esta importación para leer el JSON!
import os # ¡Añade esta importación para manejar rutas de archivos!

class Command(BaseCommand):
    help = 'Importa datos de ligas, equipos y partidos de prueba para desarrollo.'

    def _make_request(self, endpoint):
        url = f"{settings.THESPORTSDB_API_BASE_URL}{settings.THESPORTSDB_API_KEY}/{endpoint}"
        try:
            response = requests.get(url)
            response.raise_for_status() # Lanza un HTTPError para 4xx/5xx
            return response.json()
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Error al conectar con TheSportsDB API: {e}"))
            return None

    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP_INFO('Iniciando importación de datos de prueba...'))

        # Ruta al archivo JSON de datos de prueba
        json_file_path = os.path.join(os.path.dirname(__file__), 'data.json')

        # Cargar datos desde el archivo JSON
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                all_data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Error: El archivo {json_file_path} no fue encontrado."))
            return
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f"Error al decodificar el JSON en {json_file_path}: {e}"))
            return

        ligas_data = all_data.get('ligas', [])

        # --- 1. Crear Ligas ---
        self.stdout.write(self.style.HTTP_INFO('Creando ligas de prueba...'))
        ligas_creadas = {}
        for data in ligas_data:
            liga, created = Liga.objects.update_or_create(
                thesportsdb_id=data['thesportsdb_id'],
                defaults={
                    'nombre': data['nombre'],
                    'pais': data['pais'],
                    'deporte': data['deporte']
                }
            )
            ligas_creadas[data['thesportsdb_id']] = liga
            if created:
                self.stdout.write(self.style.SUCCESS(f"  Liga '{liga.nombre}' creada."))
            else:
                self.stdout.write(self.style.MIGRATE_HEADING(f"  Liga '{liga.nombre}' actualizada."))

        # --- 2. Crear Equipos de Prueba ---
        self.stdout.write(self.style.HTTP_INFO('Creando equipos de prueba...'))
        for liga_data in ligas_data:
            liga_obj = ligas_creadas.get(liga_data['thesportsdb_id'])
            if liga_obj:
                for equipo_data in liga_data.get('equipos', []):
                    equipo, created = Equipo.objects.update_or_create(
                        thesportsdb_id=equipo_data['thesportsdb_id'],
                        defaults={
                            'nombre': equipo_data['nombre'],
                            'logo_url': equipo_data.get('logo_url'),
                            'liga': liga_obj
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"    Equipo '{equipo.nombre}' creado."))
                    else:
                        self.stdout.write(self.style.MIGRATE_HEADING(f"    Equipo '{equipo.nombre}' actualizado."))
            else:
                self.stdout.write(self.style.WARNING(f"  Liga '{liga_data['nombre']}' no encontrada para crear equipos."))

        # --- 3. Crear Partidos de Prueba ---
        self.stdout.write(self.style.HTTP_INFO('Creando partidos de prueba...'))
        for liga_data in ligas_data:
            liga_obj = ligas_creadas.get(liga_data['thesportsdb_id'])
            if liga_obj:
                for partido_data in liga_data.get('partidos', []):
                    # Buscar los objetos Equipo por nombre y liga
                    equipo_local_obj = Equipo.objects.filter(
                        nombre=partido_data['equipo_local_nombre'],
                        liga=liga_obj
                    ).first()
                    equipo_visitante_obj = Equipo.objects.filter(
                        nombre=partido_data['equipo_visitante_nombre'],
                        liga=liga_obj
                    ).first()

                    if not equipo_local_obj or not equipo_visitante_obj:
                        self.stdout.write(self.style.WARNING(
                            f"    Saltando partido (equipos no encontrados): {partido_data.get('equipo_local_nombre')} vs {partido_data.get('equipo_visitante_nombre')}"))
                        continue

                    partido, created = Partido.objects.update_or_create(
                        thesportsdb_id=partido_data['thesportsdb_id'],
                        defaults={
                            'liga': liga_obj,
                            'equipo_local': equipo_local_obj,
                            'equipo_visitante': equipo_visitante_obj,
                            'fecha': datetime.datetime.strptime(partido_data['fecha'], '%Y-%m-%d').date(),
                            'hora': datetime.datetime.strptime(partido_data['hora'], '%H:%M:%S').time(),
                            'resultado_local': partido_data['resultado_local'],
                            'resultado_visitante': partido_data['resultado_visitante'],
                            'status_partido': partido_data['status_partido'] # <--- ¡CAMBIO CRUCIAL AQUÍ!
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"    Partido '{partido.equipo_local.nombre} vs {partido.equipo_visitante.nombre}' creado."))
                    else:
                        self.stdout.write(self.style.MIGRATE_HEADING(f"    Partido '{partido.equipo_local.nombre} vs {partido.equipo_visitante.nombre}' actualizado."))
            else:
                self.stdout.write(self.style.WARNING(f"  Liga '{liga_data['nombre']}' no encontrada para crear partidos."))

        self.stdout.write(self.style.SUCCESS('Importación de datos de prueba completada.'))