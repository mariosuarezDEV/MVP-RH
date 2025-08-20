# vistas
from django.views.generic import (
    CreateView,
    UpdateView,
    RedirectView,
    DetailView,
    ListView,
    TemplateView,
)

# Modelos
from .models import TurnosModel, PlantillaModel

# Formularios


# Mixins
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Shortcuts
from django.urls import reverse_lazy
from django.shortcuts import redirect

# Otros
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.utils import timezone


User = get_user_model()


def obtener_plantilla(sucursal=None):
    # Obtener la hora actual
    hora_actual = timezone.localtime().strftime("%H:%M:%S")
    # Obtener el turno que se encuentre activo
    turno_actual = TurnosModel.objects.filter(
        hora_inicio__lte=hora_actual, hora_fin__gte=hora_actual
    ).first()
    print(f"Turno actual: {turno_actual}")
    # Obtener dia en el que estamos YYYY-MM-DD
    dia = timezone.localtime().strftime("%Y-%m-%d")
    # Obtener plantilla
    if sucursal:
        print(
            f"Obteniendo plantilla para la sucursal: {sucursal} y dia: {dia} y turno: {turno_actual}"
        )
        plantilla = PlantillaModel.objects.filter(
            dia=dia, turno=turno_actual, sucursal=sucursal
        ).first()
    else:
        print(
            f"Obteniendo plantilla sin sucursal del dia: {dia} y turno: {turno_actual}"
        )
        plantilla = PlantillaModel.objects.filter(dia=dia, turno=turno_actual).first()
        print(f"Plantilla obtenida: {plantilla}")
    return plantilla


class PlantillaActualView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = "horarios.view_plantillamodel"
    template_name = "plantilla.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        plantilla = obtener_plantilla(user.sucursal)
        empleados = plantilla.empleados.all() if plantilla else []
        context["empleados"] = empleados
        return context
