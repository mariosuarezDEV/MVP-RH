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
from django.shortcuts import redirect

# Otros
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils.safestring import mark_safe


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
        context["empleado"] = (
            User.objects.filter(id=self.kwargs.get("empleado_id"))
            .select_related("sucursal", "puesto", "salario")
            .first()
        )
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
        # Regresar a la página anterior y sino regresar al perfil del empleado
        return self.request.META.get(
            "HTTP_REFERER", reverse_lazy("perfil", kwargs={"pk": incidencia.usuario.id})
        )


class RechazarIncidenciaView(LoginRequiredMixin, PermissionRequiredMixin, RedirectView):
    permission_required = "incidencias.change_bitacoramodel"

    def get_redirect_url(self, *args, **kwargs):
        incidencia = BitacoraModel.objects.get(id=self.kwargs.get("pk"))
        incidencia.estado = "rechazada"
        incidencia.user_modificacion = self.request.user
        incidencia.save()
        messages.success(self.request, "La incidencia fue rechazada.")
        # Regresar a la página anterior y sino regresar al perfil del empleado
        return self.request.META.get(
            "HTTP_REFERER", reverse_lazy("perfil", kwargs={"pk": incidencia.usuario.id})
        )


class EditarIncidenciaView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "incidencias.change_bitacoramodel"
    model = BitacoraModel
    template_name = "editar_incidencia.html"
    form_class = NuevaIncidenciaForm
    # Cache del objeto para evitar consultas duplicadas
    _object_cache = None

    def get_object(self, queryset=None):
        """Sobrescribir get_object para optimizar consultas y cachear el resultado"""
        if self._object_cache is None:
            self._object_cache = (
                BitacoraModel.objects.filter(id=self.kwargs.get("pk"))
                .select_related("usuario", "incidencia", "salario")
                .first()
            )
        return self._object_cache

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()  # Obtener el objeto de la incidencia
        if obj.estado != "en_proceso":
            mensaje = f"La incidencia <strong>{obj.incidencia.nombre}</strong> de <strong>{obj.usuario.get_full_name()}</strong> no puede ser modificada despues de haber sido resuelta o rechazada."
            messages.error(request, mark_safe(mensaje))
            # Usar redirect() en lugar de retornar una URL string
            referer = request.META.get("HTTP_REFERER")
            if referer:
                return redirect(referer)
            else:
                return redirect("perfil", pk=obj.usuario.id)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("perfil", kwargs={"pk": self.get_object().usuario.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Asegurar que 'incidencia' esté disponible en el template
        context["incidencia"] = self.get_object()
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
        context["empleado"] = (
            User.objects.filter(id=self.kwargs.get("empleado_id"))
            .select_related("sucursal", "puesto", "salario")
            .first()
        )
        return context

    def get_queryset(self):
        incidencias = (
            BitacoraModel.objects.filter(usuario=self.kwargs.get("empleado_id"))
            .select_related(
                "incidencia",
                "incidencia__tipo",
                "usuario",
                "usuario__sucursal",
                "usuario__puesto",
                "usuario__salario",
                "user_creacion",
                "user_modificacion",
            )
            .order_by("-fecha_incidencia")
        )
        return list(incidencias)


class IncidenciasView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "incidencias.view_bitacoramodel"
    model = BitacoraModel
    context_object_name = "incidencias"
    template_name = "incidencias.html"
    paginate_by = 10

    def get_queryset(self):
        return list(
            BitacoraModel.objects.all()
            .select_related(
                "usuario",
                "incidencia",
                "incidencia__tipo",
                "salario",
            )
            .order_by("-fecha_incidencia")
        )
