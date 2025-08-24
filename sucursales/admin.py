from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import SucursalModel

# Register your models here.


@admin.register(SucursalModel)
class SucursalAdmin(ModelAdmin):
    list_display = ("id", "empresa", "nombre")
    search_fields = ("nombre",)
    readonly_fields = ("created_at", "updated_at", "user_creacion", "user_modificacion")
    fieldsets = (
        (
            "Información",
            {
                "fields": (
                    "empresa",
                    "nombre",
                )
            },
        ),
        (
            "Auditoria",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                    "user_creacion",
                    "user_modificacion",
                    "active",
                )
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Si es nuevo
            obj.user_creacion = request.user
        obj.user_modificacion = request.user
        super().save_model(request, obj, form, change)
