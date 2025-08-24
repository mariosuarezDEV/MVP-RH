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
from .models import SucursalModel

# Formularios
from .forms import SucursalForm
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


class SucursalesListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "sucursales.view_sucursalmodel"
    model = SucursalModel
    template_name = "sucursales_list.html"
    context_object_name = "sucursales"

    def get_queryset(self):
        cache_key = "sucursales"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        queryset = list(
            SucursalModel.objects.filter(active=True).select_related("empresa")
        )
        cache.set(cache_key, queryset, 60 * 60)  # Cache for 1 hour
        return queryset


class CrearSucursalView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "sucursales.add_sucursalmodel"
    model = SucursalModel
    form_class = SucursalForm
    template_name = "sucursal_form.html"
    success_url = reverse_lazy("sucursales_list")

    def form_valid(self, form):
        form.instance.user_creacion = self.request.user
        form.instance.user_modificacion = self.request.user
        messages.success(self.request, "Sucursal creada correctamente.")
        return super().form_valid(form)


class EditarSucursalView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "sucursales.change_sucursalmodel"
    model = SucursalModel
    form_class = SucursalForm
    template_name = "sucursal_form.html"
    success_url = reverse_lazy("sucursales_list")

    def form_valid(self, form):
        form.instance.user_modificacion = self.request.user
        messages.success(self.request, "Sucursal editada correctamente.")
        return super().form_valid(form)


class EliminarSucursalView(LoginRequiredMixin, PermissionRequiredMixin, RedirectView):
    permission_required = "sucursales.delete_sucursalmodel"
    model = SucursalModel
    template_name = "sucursal_confirm_delete.html"
    success_url = reverse_lazy("sucursales_list")

    def get_redirect_url(self, *args, **kwargs):
        instancia = get_object_or_404(SucursalModel, pk=kwargs["pk"])
        instancia.active = False
        instancia.save()
        messages.success(self.request, "Sucursal eliminada correctamente.")
        return self.success_url
