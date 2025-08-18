from django.urls import path, include

from .views import HomeView, PerfilView

urlpatterns = [
    path("", HomeView.as_view(), name="inicio"),
    path("empleado/<int:pk>/", PerfilView.as_view(), name="perfil"),
]
