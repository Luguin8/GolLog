from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static

# Importa todas las vistas necesarias
from core.views import LigaViewSet, EquipoViewSet, RegisterView # Corregido
from partidos.views import PartidoViewSet, CalificacionViewSet, PartidoRecienteViewSet
from perfiles.views import PerfilViewSet, UserProfileViewSet, UserViewSet

# Crea el enrutador
router = DefaultRouter()

# Registra las vistas con el enrutador
router.register(r'ligas', LigaViewSet)
router.register(r'equipos', EquipoViewSet)
router.register(r'partidos', PartidoViewSet)
router.register(r'calificaciones', CalificacionViewSet)
router.register(r'users', UserViewSet)
router.register(r'partidos-recientes', PartidoRecienteViewSet, basename='partidos-recientes')
router.register(r'perfiles', PerfilViewSet, basename='perfil')
router.register(r'user-profiles', UserProfileViewSet, basename='user-profile')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='register'), # Nueva URL para el registro
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
