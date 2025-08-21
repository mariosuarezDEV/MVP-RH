from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from incidencias.models import BitacoraModel
from horarios.models import TurnosModel, PlantillaModel
from django.utils import timezone
from horarios.views import obtener_plantilla

User = get_user_model()

from incidencias.models import BitacoraModel


class HomeView(TemplateView):
    template_name = "index.html"


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_empleados"] = User.objects.count()
        context["total_incidencias"] = BitacoraModel.objects.filter(
            estado="en_proceso"
        ).count()
        context["empleado"] = self.request.user
        context["incidencias"] = BitacoraModel.objects.filter(
            estado="en_proceso"
        ).order_by("-fecha_incidencia")[:10]
        plantilla = obtener_plantilla()
        filtro = plantilla.empleados.filter(id=self.request.user.id)
        if filtro:
            print(f"El empleado esta en turno")
            context["sucursal"] = plantilla.sucursal.nombre
            context["activo"] = True
        else:
            print(f"El empleado no esta en turno")
            context["activo"] = False
        plantilla_completa = obtener_plantilla()
        empleados = plantilla_completa.empleados.all()[:6] if plantilla_completa else []
        context["empleados"] = empleados
        # Cumpleaños
        context["cumpleanos"] = [
            empleado
            for empleado in empleados
            if empleado.nacimiento and empleado.nacimiento.month == timezone.now().month
        ]

        return context


class PerfilView(LoginRequiredMixin, DetailView):
    template_name = "perfil.html"
    model = User
    context_object_name = "empleado"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["incidencias"] = BitacoraModel.objects.filter(
            usuario=self.object, estado="en_proceso"
        ).order_by("-fecha_incidencia")[:10]
        plantilla = obtener_plantilla()
        filtro = plantilla.empleados.filter(id=self.object.id)
        if filtro:
            context["sucursal"] = plantilla.sucursal.nombre
            context["activo"] = True
        else:
            context["activo"] = False
        return context
