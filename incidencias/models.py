from django.db import models
from base.models import Base
from django.contrib.auth import get_user_model
from djmoney.models.fields import MoneyField
from salarios.models import SalarioModel

User = get_user_model()


# Create your models here.
class TipoIncidenciaModel(Base):
    nombre = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text="Nombre del agrupador de incidencias",
    )

    class Meta:
        verbose_name = "Tipo de Incidencia"
        verbose_name_plural = "Tipos de Incidencias"
        db_table = "grupo_incidencias"

    def __str__(self):
        return self.nombre


class IncidenciasModel(Base):
    tipo = models.ForeignKey(
        TipoIncidenciaModel,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        verbose_name="Tipo de Incidencia",
        help_text="Tipo de incidencia a la que pertenece",
        db_index=True,
    )
    nombre = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        verbose_name="Nombre de la Incidencia",
        help_text="Nombre breve de la incidencia",
    )
    prompt = models.TextField(
        blank=False,
        null=False,
        verbose_name="Descripción de la Incidencia",
        help_text="Descripción detallada de la incidencia",
    )

    class Meta:
        verbose_name = "Incidencia"
        verbose_name_plural = "Incidencias"
        db_table = "incidencias"

    def __str__(self):
        return f"{self.tipo} - {self.nombre}"


ESTADOS_INCIDENCIA = (
    ("en_proceso", "En Proceso"),
    ("resuelta", "Resuelta"),
    ("rechazada", "Rechazada"),
)


class BitacoraModel(Base):
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        verbose_name="Usuario",
        help_text="Usuario al que se le aplica la incidencia",
        db_index=True,
    )
    incidencia = models.ForeignKey(
        IncidenciasModel,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        verbose_name="Incidencia",
        help_text="Incidencia que se trata",
        db_index=True,
    )
    nota = models.TextField(
        blank=True,
        null=True,
        verbose_name="Nota",
        help_text="Nota adicional sobre la incidencia",
    )
    monto = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="MXN",
        verbose_name="Monto",
        help_text="Monto asociado a la incidencia",
        null=True,
        blank=True,
        default=0.00,
    )
    fecha_incidencia = models.DateField(
        verbose_name="Fecha de Incidencia",
        help_text="Fecha en que se registró la incidencia",
        db_index=True,
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS_INCIDENCIA,
        default="en_proceso",
        verbose_name="Estado",
        help_text="Estado actual de la incidencia",
        db_index=True,
    )
    # Detalles
    cubre_puesto = models.BooleanField(
        default=False,
        verbose_name="Cubre Puesto",
        help_text="Indica si la incidencia cubre el puesto del usuario",
        blank=True,
        null=True,
    )
    salario = models.ForeignKey(
        SalarioModel,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Puesto/Salario objetivo",
        help_text="Salario diferente al habitual si es que aplica",
        db_index=True,
    )

    class Meta:
        verbose_name = "Bitácora"
        verbose_name_plural = "Bitácoras"
        db_table = "bitacoras"
        indexes = [
            models.Index(
                fields=["estado", "-fecha_incidencia"], name="idx_estado_fecha"
            ),
        ]

    def __str__(self):
        return f"Bitácora de {self.usuario} - {self.incidencia} - {self.estado}"
