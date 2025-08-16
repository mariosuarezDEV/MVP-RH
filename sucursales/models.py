from django.db import models
from base.models import Base
from empresas.models import EmpresaModel


# Create your models here.
class SucursalModel(Base):
    empresa = models.ForeignKey(
        EmpresaModel,
        on_delete=models.PROTECT,
        verbose_name="Empresa",
        related_name="%(class)s_sucursales",
        help_text="Seleccione la empresa a la que pertenece esta sucursal",
        null=False,
        blank=False,
    )
    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre de la sucursal",
        blank=False,
        null=False,
        help_text="Ingrese el nombre de la sucursal",
    )

    class Meta:
        verbose_name = "Sucursal"
        verbose_name_plural = "Sucursales"
        db_table = "sucursales"

    def __str__(self):
        return f"{self.nombre} - {self.empresa.nombre}"
