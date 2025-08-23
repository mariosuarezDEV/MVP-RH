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
from .models import EmpresaModel

# Formularios
from .forms import EmpresaForm
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


class EmpresasListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "empresas.view_empresamodel"
    model = EmpresaModel
    template_name = "empresa_list.html"
    context_object_name = "empresas"
    paginate_by = 10

    def get_queryset(self):
        cache_key = "empresas"
        empresas = cache.get(cache_key)
        if not empresas:
            empresas = list(
                EmpresaModel.objects.filter(active=True)
                .values("id", "nombre")
                .order_by("nombre")
            )
            cache.set(cache_key, empresas, timeout=60 * 60)  # 1 hora
        return empresas


class EmpresaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "empresas.add_empresamodel"
    model = EmpresaModel
    form_class = EmpresaForm
    template_name = "empresa_form.html"
    success_url = reverse_lazy("empresa_list")

    def form_valid(self, form):  # Personalizar si el formulario es valido
        form.instance.user_creacion = self.request.user
        form.instance.user_modificacion = self.request.user
        # Mensaje de exito
        messages.success(self.request, "La empresa ha sido creada exitosamente.")
        return super().form_valid(form)


class EmpresasUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "empresas.change_empresamodel"
    model = EmpresaModel
    form_class = EmpresaForm
    template_name = "empresa_form.html"
    success_url = reverse_lazy("empresa_list")

    def form_valid(self, form):  # Personalizar si el formulario es valido
        form.instance.user_modificacion = self.request.user
        # Mensaje de exito
        messages.success(self.request, "La empresa ha sido actualizada exitosamente.")
        return super().form_valid(form)


class EmpresaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, RedirectView):
    permission_required = "empresas.delete_empresamodel"
    model = EmpresaModel
    success_url = reverse_lazy("empresa_list")

    def get_redirect_url(self, *args, **kwargs):
        instance = get_object_or_404(EmpresaModel, pk=kwargs["pk"])
        instance.active = False
        instance.user_modificacion = self.request.user
        instance.save()
        messages.success(self.request, "La empresa ha sido eliminada exitosamente.")
        return self.success_url
