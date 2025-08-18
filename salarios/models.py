from django.db import models
from djmoney.models.fields import MoneyField
from puestos.models import PuestosModel
from base.models import Base


# Create your models here.
class SalarioModel(Base):
    monto = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="MXN",
        verbose_name="Monto",
        help_text="Monto del salario",
    )
    puesto_asociado = models.ForeignKey(
        PuestosModel, on_delete=models.SET_NULL, null=True, blank=True
    )

    descripcion = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción del salario",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Salario"
        verbose_name_plural = "Salarios"
        db_table = "salarios"

    def __str__(self):
        return (
            f" Puesto {self.puesto_asociado}"
            if self.puesto_asociado
            else f"Salario sin puesto"
        )
