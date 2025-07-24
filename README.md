# GolLog: Plataforma de Calificación de Partidos de Fútbol

## Descripción del Proyecto
GolLog es una plataforma web para que los usuarios puedan registrarse, explorar partidos de fútbol (ligas, equipos, calendarios), calificar partidos ya jugados y ver las calificaciones de otros usuarios. El objetivo es crear una comunidad alrededor de la pasión por el fútbol y la opinión sobre los encuentros.

## Tecnologías Utilizadas

### Backend (API RESTful)
* **Python 3.x:** Lenguaje de programación principal.
* **Django:** Framework web de alto nivel para un desarrollo rápido y seguro.
* **Django REST Framework (DRF):** Para construir la API RESTful que el frontend consumirá.
* **PostgreSQL:** Base de datos relacional robusta para almacenar todos los datos (ligas, equipos, partidos, calificaciones, usuarios).
* **`psycopg2-binary`:** Adaptador de PostgreSQL para Python.
* **`requests`:** Librería HTTP para interactuar con APIs externas.

### Frontend (SPA)
* **Node.js & npm:** Entorno de ejecución de JavaScript y gestor de paquetes.
* **Vue.js (Vue 3):** Framework progresivo de JavaScript para construir la interfaz de usuario.
* **Vue CLI:** Herramienta de línea de comandos para la creación y gestión de proyectos Vue.js.

## Estructura del Proyecto

```
GolLog/
├── GolLog_backend/         # Backend Django + DRF
│   ├── manage.py
│   ├── core/               # App principal
│   │   ├── models.py       # Modelos: Liga, Equipo, Partido, Calificacion
│   │   ├── serializers.py  # Serializadores DRF
│   │   ├── views.py        # ViewSets DRF
│   │   ├── urls.py         # Rutas DRF
│   │   ├── admin.py, apps.py, tests.py
│   │   ├── management/
│   │   │   └── commands/
│   │   │       ├── import_sports_data.py         # Importa datos de prueba desde JSON
│   │   │       ├── import_sports_data (thesportsdb).py # Importa datos reales desde TheSportsDB
│   │   │       └── data.json                     # Datos de ejemplo (ligas, equipos, partidos)
│   │   └── migrations/
│   ├── GolLog_backend/
│   │   ├── settings.py, settings_local.py        # Configuración Django y API Key
│   │   ├── urls.py, wsgi.py, asgi.py
│   │   └── __init__.py
├── gollog_frontend/        # Frontend Vue.js
│   ├── src/
│   │   ├── main.js         # Configuración Vue y rutas
│   │   ├── App.vue         # Layout principal
│   │   └── components/
│   │       ├── LigaList.vue    # Lista de ligas
│   │       └── EquipoList.vue  # Lista de equipos por liga
│   ├── public/index.html
│   ├── package.json, vue.config.js, babel.config.js, jsconfig.json
│   └── .gitignore
├── .gitignore
└── README.md               # Este archivo
