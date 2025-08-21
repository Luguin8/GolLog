from rest_framework import viewsets, mixins
from .models import Perfil
from .serializers import PerfilSerializer, UserProfileSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

class PerfilViewSet(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Perfil.objects.filter(usuario=user)
        return Perfil.objects.none()

class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
