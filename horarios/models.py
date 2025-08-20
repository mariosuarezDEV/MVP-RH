from django.db import models
from sucursales.models import SucursalModel
from base.models import Base
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.


class TurnosModel(Base):
    nombre = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        help_text="Nombre del turno",
        verbose_name="Turno",
    )
    hora_inicio = models.TimeField(
        blank=False,
        null=False,
        help_text="Hora de inicio del turno",
        verbose_name="Hora de inicio",
    )
    hora_fin = models.TimeField(
        blank=False,
        null=False,
        help_text="Hora de fin del turno",
        verbose_name="Hora de fin",
    )

    class Meta:
        verbose_name = "Turno"
        verbose_name_plural = "Turnos"
        db_table = "turnos"

    def __str__(self):
        return self.nombre


class PlantillaModel(Base):
    # Empleados que trabajan X dia y X turno
    sucursal = models.ForeignKey(
        SucursalModel,
        on_delete=models.PROTECT,
        related_name="%(class)s_plantillas",
        help_text="Sucursal donde se trabaja",
        verbose_name="Sucursal",
    )
    dia = models.DateField(
        blank=False,
        null=False,
        help_text="Día de trabajo",
        verbose_name="Día",
    )
    turno = models.ForeignKey(
        TurnosModel,
        on_delete=models.CASCADE,
        related_name="plantillas",
        help_text="Turno de trabajo",
        verbose_name="Turno",
    )
    empleados = models.ManyToManyField(
        User,
        related_name="plantillas",
        help_text="Empleados asignados",
        verbose_name="Empleados",
    )

    class Meta:
        verbose_name = "Plantilla"
        verbose_name_plural = "Plantillas"
        db_table = "plantillas"

    def __str__(self):
        return f"Plantilla {self.id} - {self.sucursal} - {self.dia} - {self.turno}"
