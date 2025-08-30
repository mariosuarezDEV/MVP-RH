from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HomeView, PerfilView, DashboardView
from .viewsets import UsuariosViewSet

router = DefaultRouter()

router.register(r"usuarios", UsuariosViewSet, basename="usuarios")

urlpatterns = [
    path("", DashboardView.as_view(), name="inicio"),
    path("empleado/<int:pk>/", PerfilView.as_view(), name="perfil"),
    path("api/", include(router.urls)),
]
