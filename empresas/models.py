from django.db import models
from base.models import Base

# Create your models here.


class EmpresaModel(Base):
    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre de la Empresa",
        help_text="Nombre de la Empresa",
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        db_table = "empresas"

    def __str__(self):
        return self.nombre
