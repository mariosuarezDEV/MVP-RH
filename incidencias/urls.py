from django.urls import path
from .views import (
    NuevaIncidenciaView,
    AceptarIncidenciaView,
    RechazarIncidenciaView,
    EditarIncidenciaView,
    InformacionIncidenciaView,
    HistorialIncidenciasView,
)

urlpatterns = [
    path(
        "nueva/<int:empleado_id>/",
        NuevaIncidenciaView.as_view(),
        name="nueva_incidencia",
    ),
    path(
        "aceptar/<int:pk>/",
        AceptarIncidenciaView.as_view(),
        name="aceptar_incidencia",
    ),
    path(
        "rechazar/<int:pk>/",
        RechazarIncidenciaView.as_view(),
        name="rechazar_incidencia",
    ),
    path(
        "editar/<int:pk>/",
        EditarIncidenciaView.as_view(),
        name="editar_incidencia",
    ),
    path(
        "informacion/<int:pk>/",
        InformacionIncidenciaView.as_view(),
        name="informacion_incidencia",
    ),
    path(
        "historial/<int:empleado_id>/",
        HistorialIncidenciasView.as_view(),
        name="historial_incidencias",
    ),
]
