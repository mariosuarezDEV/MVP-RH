from django.urls import path, include

from .views import HomeView, PerfilView, DashboardView

urlpatterns = [
    path("", DashboardView.as_view(), name="inicio"),
    path("empleado/<int:pk>/", PerfilView.as_view(), name="perfil"),
]
