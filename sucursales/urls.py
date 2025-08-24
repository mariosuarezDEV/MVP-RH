from django.urls import path
from .views import (
    SucursalesListView,
    CrearSucursalView,
    EditarSucursalView,
    EliminarSucursalView,
)

urlpatterns = [
    path("", SucursalesListView.as_view(), name="sucursales_list"),
    path("crear/", CrearSucursalView.as_view(), name="sucursal_create"),
    path("editar/<int:pk>/", EditarSucursalView.as_view(), name="sucursal_edit"),
    path("eliminar/<int:pk>/", EliminarSucursalView.as_view(), name="sucursal_delete"),
]
