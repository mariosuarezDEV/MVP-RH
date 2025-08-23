from django.urls import path
from .views import (
    EmpresasListView,
    EmpresaCreateView,
    EmpresasUpdateView,
    EmpresaDeleteView,
)

urlpatterns = [
    path("", EmpresasListView.as_view(), name="empresa_list"),
    path("agregar/", EmpresaCreateView.as_view(), name="empresa_create"),
    path("editar/<int:pk>/", EmpresasUpdateView.as_view(), name="empresa_update"),
    path("eliminar/<int:pk>/", EmpresaDeleteView.as_view(), name="empresa_delete"),
]
