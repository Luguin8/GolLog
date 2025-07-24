from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core import views # Importa las vistas que definiste en core/views.py

# Crea un enrutador por defecto
router = DefaultRouter()
# Registra tus ViewSets con el enrutador
router.register(r'ligas', views.LigaViewSet)
router.register(r'equipos', views.EquipoViewSet)
router.register(r'partidos', views.PartidoViewSet)
router.register(r'calificaciones', views.CalificacionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Incluye las URLs generadas por el enrutador de DRF bajo el prefijo 'api/'
    path('api/', include(router.urls)),
    # Opcional: Esto añade URLs para el login/logout en el navegador para DRF.
    path('api/', include('core.urls')),  # Incluye las URLs de tu aplicación core
    # Útil para probar la API directamente en el navegador.
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]