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
from .models import TurnosModel, PlantillaModel

# Formularios
from .forms import (
    PlantillaForm,
    DiaTurnoForm,
    EmpleadosSucursalForm,
    OtrosEmpleadosForm,
)
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


def obtener_plantilla(sucursal=None, usuario=None):
    """Sirve para obtener el grupo de empleados segun el turno y sucursal actual"""
    # Agregamos usuario ya que sera el que busquemos en las plantillas obtenidas
    try:
        hora = timezone.localtime()
        hora_actual = hora.time()
        dia_actual = hora.date()

        # # Cachear turno actual por 60 minutos
        turno_cache_key = f"turno_actual_{hora_actual.hour}_{hora_actual.minute // 30}"
        turno_actual = cache.get(turno_cache_key)

        if not turno_actual:  # No existe en caché
            # Obtener el turno actual
            turno_actual = TurnosModel.objects.filter(
                hora_inicio__lte=hora_actual, hora_fin__gte=hora_actual
            ).first()
            if turno_actual:
                cache.set(
                    turno_cache_key, turno_actual, 60 * 60
                )  # Cachear por 60 minutos
            else:
                logger.warning(
                    "No se encontró un turno actual para la hora %s", hora_actual
                )
                return None
        # print(f"Turno actual cacheado: {turno_actual}")
        filtros = {"turno": turno_actual, "dia": dia_actual}
        if sucursal:
            filtros["sucursal"] = sucursal
        if usuario:
            filtros["empleados"] = usuario
        # print(f"Filtros para obtener plantilla: {filtros}")
        plantilla = (
            PlantillaModel.objects.filter(**filtros)
            .select_related("sucursal", "turno")
            .prefetch_related("empleados")
            .first()
        )
        if not plantilla:
            return None
        return plantilla
    except Exception as e:
        logger.error("Error al obtener la hora actual: %s", e)
        return None


class PlantillaActualView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = "horarios.view_plantillamodel"
    template_name = "plantilla.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = (
            User.objects.filter(id=self.request.user.id)
            .select_related("sucursal", "puesto", "salario")
            .first()
        )
        plantilla = obtener_plantilla(user.sucursal)
        empleados = list(
            plantilla.empleados.all().select_related("sucursal", "puesto", "salario")
            if plantilla
            else []
        )
        context["empleados"] = empleados
        return context


class CrearPlantillaView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "horarios.add_plantillamodel"
    # Pasar la sucursal del usuario logueado
    form_class = PlantillaForm
    template_name = "crear_plantilla.html"

    def get_success_url(self):
        return self.request.META.get("HTTP_REFERER", reverse_lazy("inicio"))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["sucursal"] = self.request.user.sucursal_id
        return kwargs

    def form_valid(self, form):
        form.instance.sucursal_id = self.request.user.sucursal_id
        form.instance.user_creacion = self.request.user
        form.instance.user_modificacion = self.request.user
        # Mensaje
        messages.success(
            self.request,
            f"Tu horario del dia {form.instance.dia} se subió correctamente para el turno {form.instance.turno.nombre}.",
        )
        return super().form_valid(form)


class VerPlantillasView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "horarios.view_plantillamodel"
    model = PlantillaModel
    template_name = "plantillas.html"
    context_object_name = "plantillas"
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        dia = timezone.localtime().date()
        # obtener la plantilla de la fecha actual en adelante
        return list(
            super()
            .get_queryset()
            .filter(sucursal=user.sucursal, dia__gte=dia)
            .select_related("turno", "sucursal", "sucursal__empresa")
            .prefetch_related("empleados")
            .order_by("dia")
        )


class DetallePlantillaView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = "horarios.view_plantillamodel"
    model = PlantillaModel
    template_name = "detalle_plantilla.html"
    context_object_name = "plantilla"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("sucursal", "turno")
            .prefetch_related(
                "empleados",
                "empleados__puesto",
                "empleados__sucursal",
            )
        )


class EliminarPlantillaView(LoginRequiredMixin, PermissionRequiredMixin, RedirectView):
    permission_required = "horarios.delete_plantillamodel"
    model = PlantillaModel
    context_object_name = "plantilla"

    def get_redirect_url(self, *args, **kwargs):
        plantilla = PlantillaModel.objects.get(pk=kwargs["pk"])
        try:
            plantilla.delete()
            messages.success(self.request, "Plantilla eliminada correctamente.")
        except Exception as e:
            # Mensaje de error
            messages.error(self.request, "Error al eliminar la plantilla.")
        return reverse_lazy("ver_plantillas")


class EditarPlantillaView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "horarios.change_plantillamodel"
    model = PlantillaModel
    form_class = PlantillaForm
    template_name = "editar_plantilla.html"

    def get_success_url(self):
        return self.request.META.get("HTTP_REFERER", reverse_lazy("inicio"))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["sucursal"] = self.request.user.sucursal_id
        return kwargs

    def form_valid(self, form):
        form.instance.sucursal_id = self.request.user.sucursal_id
        form.instance.user_modificacion = self.request.user
        # Mensaje
        messages.success(
            self.request,
            f"Tu horario del dia {form.instance.dia} se actualizo correctamente para el turno {form.instance.turno.nombre}.",
        )
        return super().form_valid(form)


class CrearPlantillaWizard(SessionWizardView):
    form_list = [
        ("0", DiaTurnoForm),
        ("1", EmpleadosSucursalForm),
        ("2", OtrosEmpleadosForm),
    ]
    template_name = "crear_plantilla_wizard.html"

    def get_form_kwargs(self, step=None):
        """Pasar la sucursal del usuario a los formularios de empleados"""
        kwargs = super().get_form_kwargs(step)
        if step in ["1", "2"]:
            kwargs["sucursal"] = self.request.user.sucursal_id
        return kwargs

    def done(self, form_list, **kwargs):
        # Aquí puedes procesar los datos de todos los formularios
        # y crear la plantilla en la base de datos
        turno = form_list[0]
        empleados_suc = form_list[1]
        otros_empleados = form_list[2]
        # Crear la plantilla
        plantilla = PlantillaModel.objects.create(
            sucursal=self.request.user.sucursal,
            dia=turno.cleaned_data["dia"],
            turno=turno.cleaned_data["turno"],
            user_creacion=self.request.user,
            user_modificacion=self.request.user,
        )
        # Agregar empleados a la plantilla
        empleados_sucursal = empleados_suc.cleaned_data["empleados"]
        otros = otros_empleados.cleaned_data["otros_empleados"]
        plantilla.empleados.add(*empleados_sucursal, *otros)
        # Mensaje de exito
        messages.success(self.request, "Plantilla creada correctamente.")
        return redirect("ver_plantillas")


class EditarPlantillaWizard(SessionWizardView):
    form_list = [
        ("0", DiaTurnoForm),
        ("1", EmpleadosSucursalForm),
        ("2", OtrosEmpleadosForm),
    ]
    template_name = "crear_plantilla_wizard.html"

    def dispatch(self, request, *args, **kwargs):
        """Cargar la plantilla a editar antes de procesar cualquier paso"""
        self.plantilla = get_object_or_404(PlantillaModel, pk=self.kwargs.get("pk"))
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self, step=None):
        """Pasar la sucursal a los formularios de empleados"""
        kwargs = super().get_form_kwargs(step)
        if step in ["1", "2"]:
            kwargs["sucursal"] = self.request.user.sucursal_id
        return kwargs

    def get_form_initial(self, step):
        """Inicializar los formularios con los datos existentes"""
        if step == "0":  # Dia y turno
            return {
                "dia": self.plantilla.dia,
                "turno": self.plantilla.turno,
            }
        elif step == "1":  # Empleados de la sucursal
            empleados_sucursal = self.plantilla.empleados.filter(
                sucursal_id=self.request.user.sucursal_id
            )
            return {"empleados": empleados_sucursal}
        elif step == "2":  # Otros empleados
            otros_empleados = self.plantilla.empleados.exclude(
                sucursal_id=self.request.user.sucursal_id
            )
            return {"otros_empleados": otros_empleados}
        return {}

    def done(self, form_list, **kwargs):
        # Actualizar datos generales
        turno = form_list[0]
        empleados_suc = form_list[1]
        otros_empleados = form_list[2]

        self.plantilla.dia = turno.cleaned_data["dia"]
        self.plantilla.turno = turno.cleaned_data["turno"]
        self.plantilla.user_modificacion = self.request.user
        self.plantilla.save()

        # Actualizar empleados
        empleados_sucursal = empleados_suc.cleaned_data["empleados"]
        otros = otros_empleados.cleaned_data["otros_empleados"]
        self.plantilla.empleados.set(list(empleados_sucursal) + list(otros))

        # Mensaje de éxito
        messages.success(self.request, "Plantilla actualizada correctamente.")
        return redirect("ver_plantillas")
