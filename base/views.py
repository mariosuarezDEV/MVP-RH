from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from incidencias.models import BitacoraModel

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
        return context
