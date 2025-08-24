# vistas
from django.views.generic import (
    CreateView,
    UpdateView,
    RedirectView,
    DetailView,
    DeleteView,
    ListView,
    TemplateView,
)

# Modelos
from .models import PuestosModel

# Formularios
from .forms import PuestosForm
from formtools.wizard.views import SessionWizardView

# Mixins
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Shortcuts
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404

# Otros
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.utils import timezone
import logging
from django.core.cache import cache
from django.db import connection

logger = logging.getLogger(__name__)

User = get_user_model()


class PuestoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "puestos.view_puestos"
    model = PuestosModel
    template_name = "puestos_list.html"
    context_object_name = "puestos"

    def get_queryset(self):
        cache_key = "puestos"
        puestos = cache.get(cache_key)
        if puestos is None:
            puestos = list(
                PuestosModel.objects.filter(active=True).values(
                    "id", "nombre", "descripcion"
                )
            )
            cache.set(cache_key, puestos)
        return puestos


class CrearPuestoView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "puestos.add_puestos"
    model = PuestosModel
    form_class = PuestosForm
    template_name = "puesto_form.html"
    success_url = reverse_lazy("puestos_list")

    def form_valid(self, form):
        form.instance.user_creacion = self.request.user
        form.instance.user_modificacion = self.request.user
        return super().form_valid(form)


class EditarPuestoView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "puestos.change_puestos"
    model = PuestosModel
    form_class = PuestosForm
    template_name = "puesto_form.html"
    success_url = reverse_lazy("puestos_list")

    def form_valid(self, form):
        form.instance.user_modificacion = self.request.user
        return super().form_valid(form)


class EliminarPuestoView(LoginRequiredMixin, PermissionRequiredMixin, RedirectView):
    permission_required = "puestos.delete_puestos"
    model = PuestosModel

    def get_redirect_url(self, *args, **kwargs):
        """Cambiar el active del objeto a False"""
        instance = get_object_or_404(PuestosModel, pk=kwargs["pk"])
        instance.active = False
        instance.save()
        messages.success(self.request, "Puesto eliminado con éxito.")
        return super().get_redirect_url(*args, **kwargs)
