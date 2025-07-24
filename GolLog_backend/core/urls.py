from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Crear un router para registrar automáticamente las vistas de ViewSet
router = DefaultRouter()
router.register(r'ligas', views.LigaViewSet)
router.register(r'equipos', views.EquipoViewSet)
router.register(r'partidos', views.PartidoViewSet)
router.register(r'calificaciones', views.CalificacionViewSet)

urlpatterns = [
    # Las URLs generadas por el router
    path('', include(router.urls)),
    # Puedes añadir URLs manuales aquí si necesitas rutas personalizadas
]