# vistas
from django.views.generic import (
    CreateView,
    UpdateView,
    RedirectView,
    DetailView,
    ListView,
)

# Modelos
from .models import BitacoraModel

# Formularios
from .forms import NuevaIncidenciaForm

# Mixins
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Shortcuts
from django.urls import reverse_lazy

# Otros
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()

# Create your views here.


class NuevaIncidenciaView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "incidencias.add_bitacoramodel"
    model = BitacoraModel
    template_name = "nueva_incidencia.html"
    form_class = NuevaIncidenciaForm
    # Regresar al perfil del empleado

    def get_success_url(self):
        return reverse_lazy("perfil", kwargs={"pk": self.kwargs.get("empleado_id")})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["empleado"] = User.objects.get(id=self.kwargs.get("empleado_id"))
        return context

    def form_valid(self, form):
        form.instance.usuario = User.objects.get(id=self.kwargs.get("empleado_id"))
        # Campos de auditoria
        form.instance.user_creacion = self.request.user
        form.instance.user_modificacion = self.request.user

        messages.success(self.request, "La incidencia se aplico correctamente.")
        return super().form_valid(form)


class AceptarIncidenciaView(LoginRequiredMixin, PermissionRequiredMixin, RedirectView):
    permission_required = "incidencias.change_bitacoramodel"

    def get_redirect_url(self, *args, **kwargs):
        incidencia = BitacoraModel.objects.get(id=self.kwargs.get("pk"))
        incidencia.estado = "resuelta"
        incidencia.user_modificacion = self.request.user
        incidencia.save()
        messages.success(self.request, "La incidencia fue resuelta.")
        return reverse_lazy("perfil", kwargs={"pk": incidencia.usuario.id})


class RechazarIncidenciaView(LoginRequiredMixin, PermissionRequiredMixin, RedirectView):
    permission_required = "incidencias.change_bitacoramodel"

    def get_redirect_url(self, *args, **kwargs):
        incidencia = BitacoraModel.objects.get(id=self.kwargs.get("pk"))
        incidencia.estado = "rechazada"
        incidencia.user_modificacion = self.request.user
        incidencia.save()
        messages.success(self.request, "La incidencia fue rechazada.")
        return reverse_lazy("perfil", kwargs={"pk": incidencia.usuario.id})


class EditarIncidenciaView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "incidencias.change_bitacoramodel"
    model = BitacoraModel
    template_name = "editar_incidencia.html"
    form_class = NuevaIncidenciaForm

    def get_success_url(self):
        return reverse_lazy("perfil", kwargs={"pk": self.object.usuario.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["incidencia"] = self.object
        return context

    def form_valid(self, form):
        form.instance.user_modificacion = self.request.user
        messages.success(self.request, "La incidencia fue actualizada.")
        return super().form_valid(form)


class InformacionIncidenciaView(
    LoginRequiredMixin, PermissionRequiredMixin, DetailView
):
    permission_required = "incidencias.view_bitacoramodel"
    model = BitacoraModel
    template_name = "detalle_incidencia.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["incidencia"] = self.object
        return context


class HistorialIncidenciasView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "incidencias.view_bitacoramodel"
    model = BitacoraModel
    template_name = "historial_incidencias.html"
    context_object_name = "incidencias"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["empleado"] = User.objects.get(id=self.kwargs.get("empleado_id"))
        return context

    def get_queryset(self):
        return BitacoraModel.objects.filter(
            usuario=self.kwargs.get("empleado_id")
        ).order_by("-fecha_incidencia")
