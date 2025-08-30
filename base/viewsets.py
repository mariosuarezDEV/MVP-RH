from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

# Seguridad
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


class UsuariosViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
