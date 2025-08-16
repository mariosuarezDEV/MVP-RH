from django.db import models
from base.models import Base


# Create your models here.
class PuestosModel(Base):
    nombre = models.CharField(
        max_length=100, verbose_name="Nombre", help_text="Nombre del puesto"
    )
    descripcion = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción del puesto",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Puesto"
        verbose_name_plural = "Puestos"
        db_table = "puestos"

    def __str__(self):
        return self.nombre
