from django.urls import path
from .views import PlantillaActualView

urlpatterns = [
    path("", PlantillaActualView.as_view(), name="plantilla_actual"),
]
