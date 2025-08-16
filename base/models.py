from django.db import models
from django.contrib.auth.models import AbstractUser
from martor.models import MartorField

# Create your models here.


class User(AbstractUser):
    biografia = MartorField(blank=True, null=True, verbose_name="Biografía")
    puesto = models.ForeignKey(
        "puestos.PuestosModel", on_delete=models.PROTECT, null=True, blank=True
    )
    salario = models.ForeignKey(
        "salarios.SalarioModel", on_delete=models.PROTECT, null=True, blank=True
    )
    fecha_ingreso = models.DateField(
        blank=True, null=True, help_text="Fecha de ingreso a la empresa"
    )
    sucursal = models.ForeignKey(
        "sucursales.SucursalModel", on_delete=models.PROTECT, null=True, blank=True
    )


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_creacion = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="%(class)s_creacion"
    )
    user_modificacion = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="%(class)s_modificacion"
    )
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
