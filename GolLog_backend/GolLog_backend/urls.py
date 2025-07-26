from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from core import views # Importa las vistas que definiste en core/views.py
from rest_framework.authtoken.views import obtain_auth_token
from core.views import LigaViewSet, EquipoViewSet, PartidoViewSet, CalificacionViewSet  # Importa tu vista de registro si la tienes
from django.conf import settings
from django.conf.urls.static import static

# Crea un enrutador por defecto
router = routers.DefaultRouter()
# Registra tus ViewSets con el enrutador
router.register('ligas', LigaViewSet)
router.register('equipos', EquipoViewSet)
router.register('partidos', PartidoViewSet)
router.register('calificaciones', CalificacionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Incluye las URLs generadas por el enrutador de DRF bajo el prefijo 'api/'
    path('api/', include(router.urls)),
    # Opcional: Esto añade URLs para el login/logout en el navegador para DRF.
    path('api/', include('core.urls')),  # Incluye las URLs de tu aplicación core
    # Útil para probar la API directamente en el navegador.
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]

if settings.DEBUG:
    # Solo sirve archivos estáticos y de medios en modo DEBUG
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)