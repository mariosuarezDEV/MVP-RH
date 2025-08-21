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
import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)

User = get_user_model()


def obtener_plantilla(sucursal=None):
    """Sirve para obtener el grupo de empleados segun el turno y sucursal actual"""
    try:
        hora = timezone.localtime()
        hora_actual = hora.time()
        dia_actual = hora.date()

        # # Cachear turno actual por 30 minutos
        turno_cache_key = f"turno_actual_{hora_actual.hour}_{hora_actual.minute // 30}"
        turno_actual = cache.get(turno_cache_key)

        if not turno_actual:  # No existe en caché
            # Obtener el turno actual
            turno_actual = TurnosModel.objects.filter(
                hora_inicio__lte=hora_actual, hora_fin__gte=hora_actual
            ).first()
            if turno_actual:
                cache.set(
                    turno_cache_key, turno_actual, 60 * 30
                )  # Cachear por 30 minutos
            else:
                logger.warning(
                    "No se encontró un turno actual para la hora %s", hora_actual
                )
                return None
        filtros = {"turno": turno_actual, "dia": dia_actual}
        if sucursal:
            filtros["sucursal"] = sucursal
        plantilla = (
            PlantillaModel.objects.filter(**filtros)
            .select_related("sucursal", "turno")
            .prefetch_related("empleados")
            .first()
        )
        return plantilla
    except Exception as e:
        logger.error("Error al obtener la hora actual: %s", e)
        return None


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
