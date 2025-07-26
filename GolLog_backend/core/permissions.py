from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado para permitir que solo los propietarios de un objeto lo editen o eliminen.
    Los usuarios no propietarios solo tienen permisos de lectura.
    """

    def has_object_permission(self, request, view, obj):
        # Permisos de lectura están permitidos para cualquier solicitud.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Los permisos de escritura solo se otorgan al propietario del objeto.
        # Asume que la instancia del modelo tiene un atributo 'usuario'.
        return obj.usuario == request.user