from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import SalarioModel


# Register your models here.
@admin.register(SalarioModel)
class SalarioAdmin(ModelAdmin):
    list_display = ("monto", "puesto_asociado", "descripcion")
    search_fields = ("monto",)
    readonly_fields = (
        "user_creacion",
        "user_modificacion",
        "created_at",
        "updated_at",
    )
    fieldsets = (
        ("Información", {"fields": ("monto", "puesto_asociado", "descripcion")}),
        (
            "Auditoría",
            {
                "fields": (
                    "user_creacion",
                    "user_modificacion",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Si es nuevo
            obj.user_creacion = request.user
        obj.user_modificacion = request.user
        super().save_model(request, obj, form, change)
