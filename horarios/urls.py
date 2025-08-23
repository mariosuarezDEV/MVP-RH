from django.urls import path
from .views import (
    PlantillaActualView,
    CrearPlantillaView,
    VerPlantillasView,
    DetallePlantillaView,
    EliminarPlantillaView,
    EditarPlantillaView,
    CrearPlantillaWizard,
    EditarPlantillaWizard,
)

urlpatterns = [
    path("", PlantillaActualView.as_view(), name="plantilla_actual"),
    path("nuevo/", CrearPlantillaView.as_view(), name="crear_plantilla"),
    path("plantillas/", VerPlantillasView.as_view(), name="ver_plantillas"),
    path("detalle/<int:pk>/", DetallePlantillaView.as_view(), name="detalle_plantilla"),
    path(
        "eliminar/<int:pk>/", EliminarPlantillaView.as_view(), name="eliminar_plantilla"
    ),
    path("editar/<int:pk>/", EditarPlantillaView.as_view(), name="editar_plantilla"),
    path("agregar/", CrearPlantillaWizard.as_view(), name="crear_plantilla_wizard"),
    path(
        "actualizar/<int:pk>/",
        EditarPlantillaWizard.as_view(),
        name="editar_plantilla_wizard",
    ),
]
