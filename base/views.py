from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

User = get_user_model()

from incidencias.models import BitacoraModel


class HomeView(TemplateView):
    template_name = "index.html"


class PerfilView(LoginRequiredMixin, DetailView):
    template_name = "perfil.html"
    model = User
    context_object_name = "empleado"
