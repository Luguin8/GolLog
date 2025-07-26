from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView  # Importa tu vista de registro si la tienes

# Crear un router para registrar automáticamente las vistas de ViewSet
router = DefaultRouter()
router.register(r'ligas', views.LigaViewSet)
router.register(r'equipos', views.EquipoViewSet)
router.register(r'partidos', views.PartidoViewSet)
router.register(r'calificaciones', views.CalificacionViewSet)

urlpatterns = [
    # Rutas de autenticación de JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
]