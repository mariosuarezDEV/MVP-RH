from django.urls import path
from .views import PlantillaActualView, CrearPlantillaView

urlpatterns = [
    path("", PlantillaActualView.as_view(), name="plantilla_actual"),
    path("nuevo/", CrearPlantillaView.as_view(), name="crear_plantilla"),
]
