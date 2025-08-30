from django.views.generic import TemplateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import get_user_model
from incidencias.models import BitacoraModel
from django.utils import timezone
from horarios.views import obtener_plantilla
from django.db.models import Count, Q
from django.core.cache import cache

User = get_user_model()


class HomeView(TemplateView):
    template_name = "index.html"


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Optimizacion de consultas
        usuario_login = (
            User.objects.filter(id=self.request.user.id)
            .select_related("sucursal", "puesto", "salario")
            .first()
        )
        plantilla = obtener_plantilla(usuario=usuario_login)

        # Consultas optimizadas (Información básica de dashboard)
        estadisticas = self._get_estadisticas_dashboard()
        context.update(
            {
                "total_empleados": User.objects.aggregate(total=Count("id"))["total"],
                "total_incidencias": estadisticas.get("total_incidencias", 0),
                "empleado": usuario_login,
                "cumpleanos": self._get_festivos(),
            }
        )
        # Actualizamos las incidencias recientes
        context.update(self._get_incidencias_recientes())

        if plantilla:
            context.update(self._get_horario_detalles(plantilla, usuario_login))
        else:
            context.update(
                {
                    "sucursal": None,
                    "activo": False,
                    "empleados": [],
                }
            )
        return context

    def _get_estadisticas_dashboard(self):
        estadisticas = BitacoraModel.objects.aggregate(
            total_incidencias=Count("id", filter=Q(estado="en_proceso")),
        )
        return estadisticas  # regresa un diccionario

    def _get_incidencias_recientes(self):
        """Obtiene las incidencias recientes para el dashboard."""
        return {
            "incidencias": list(
                BitacoraModel.objects.filter(estado="en_proceso")
                .select_related(
                    "usuario",
                    "usuario__sucursal",
                    "usuario__puesto",
                    "incidencia",
                    "incidencia__tipo",
                    "salario__puesto_asociado",
                    "salario",
                    "user_creacion",
                    "user_modificacion",
                )
                .order_by("-fecha_incidencia")[:5]
            )
        }

    def _get_festivos(self):
        """Versión optimizada para obtener cumpleaños del mes."""
        mes_actual = timezone.now().month
        festivos_cache_key = f"cumpleanos_mes_{mes_actual}"
        cumpleanos = cache.get(festivos_cache_key)
        if not cumpleanos:
            cumpleanos = (
                User.objects.filter(
                    nacimiento__month=mes_actual, nacimiento__isnull=False
                )
                .select_related("sucursal", "puesto")
                .order_by("nacimiento__day")
            )
            cache.set(festivos_cache_key, cumpleanos, 60 * 15)
        return cumpleanos

    def _get_horario_detalles(self, plantilla, usuario_login):
        """Obtiene los detalles del horario del usuario actual."""
        context = {"sucursal": None, "empleados": [], "activo": False}
        usuario_en_plantilla = plantilla.empleados.filter(
            id=usuario_login.id
        ).exists()  # Una consulta
        if usuario_en_plantilla:
            context.update(
                {
                    "sucursal": plantilla.sucursal.nombre,
                    "activo": True,
                }
            )
        context["empleados"] = list(
            plantilla.empleados.all().select_related("sucursal", "puesto")[:6]
        )  # Una consulta
        return context


class PerfilView(LoginRequiredMixin, DetailView):
    template_name = "perfil.html"
    model = User
    context_object_name = "empleado"

    def get_queryset(self):
        return super().get_queryset().select_related("sucursal", "salario", "puesto")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plantilla = obtener_plantilla(usuario=self.object)
        # Turno de empleado
        if plantilla:
            context.update(self._get_detalles_turno(plantilla))
        else:
            context.update({"sucursal": None, "activo": False, "empleados": []})
        # Incidencias del empleado
        context.update(self._get_incidencias_empleado())
        return context

    def _get_incidencias_empleado(self):
        """Obtener las incidencias del empleado con select_related"""
        incidencias = (
            BitacoraModel.objects.filter(usuario=self.object, estado="en_proceso")
            .select_related(
                "usuario",
                "incidencia",
                "incidencia__tipo",
                "salario",
            )
            .order_by("-fecha_incidencia")[:10]
        )
        return {
            "incidencias": list(incidencias),
        }

    def _get_detalles_turno(self, plantilla):
        """Obtener los detalles del turno del empleado."""
        context = {"sucursal": None, "activo": False, "empleados": []}
        usuario_en_plantilla = plantilla.empleados.filter(id=self.object.id).exists()
        if usuario_en_plantilla:
            context.update(
                {
                    "sucursal": plantilla.sucursal.nombre,
                    "activo": True,
                }
            )
        return context


class EditarEmpleadoView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    pass
