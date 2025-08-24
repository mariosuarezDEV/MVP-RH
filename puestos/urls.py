from django.urls import path
from .views import PuestoListView, CrearPuestoView, EditarPuestoView, EliminarPuestoView


urlpatterns = [
    path("", PuestoListView.as_view(), name="puestos_list"),
    path("crear/", CrearPuestoView.as_view(), name="crear_puesto"),
    path("editar/<int:pk>/", EditarPuestoView.as_view(), name="editar_puesto"),
    path("eliminar/<int:pk>/", EliminarPuestoView.as_view(), name="eliminar_puesto"),
]
