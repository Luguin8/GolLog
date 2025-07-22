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

### Integración de Datos
* **TheSportsDB.com API:** API externa utilizada para obtener datos reales de ligas, equipos y partidos de fútbol.

## Estructura del Proyecto
GolLog/
├── venv/                   # Entorno virtual de Python (IGNORADO por Git)
├── GolLog_backend/         # Carpeta raíz del proyecto Django
│   ├── GolLog_backend/     # Archivos de configuración del proyecto Django (settings.py, urls.py, etc.)
│   │   └── settings_local.py # Archivo local para API keys (IGNORADO por Git)
│   ├── core/               # Aplicación principal de Django
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── import_sports_data.py # Comando para importar datos de TheSportsDB
│   │   ├── models.py       # Definición de los modelos de base de datos (Liga, Equipo, Partido, Calificacion)
│   │   ├── serializers.py  # Serializadores de DRF para convertir datos a/desde JSON
│   │   └── views.py        # Vistas de DRF para la API RESTful
│   ├── manage.py           # Utilidad de línea de comandos de Django
│   └── db.sqlite3          # Base de datos SQLite (IGNORADA por Git, usamos PostgreSQL)
├── .gitignore              # Archivo para ignorar archivos/carpetas en Git
└── README.md               # Este archivo de documentación

## Configuración y Ejecución del Proyecto (Backend)

Sigue estos pasos para poner en marcha el backend de GolLog en tu máquina local.

### Prerequisitos
* **Python 3.x**
* **PostgreSQL** (con `pgAdmin 4` opcional para gestión de DB)
* **Node.js y npm** (LTS recomendado)
* **Git**

### 1. Clonar el Repositorio
```bash
git clone [https://github.com/Luguin8/GolLog.git](https://github.com/Luguin8/GolLog.git)
cd GolLog