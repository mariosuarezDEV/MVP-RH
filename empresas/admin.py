from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import EmpresaModel


# Register your models here.
@admin.register(EmpresaModel)
class EmpresaAdmin(ModelAdmin):
    list_display = (
        "id",
        "nombre",
    )

    readonly_fields = ("created_at", "updated_at", "user_creacion", "user_modificacion")
    fieldsets = (
        ("Informacion", {"fields": ("nombre",)}),
        (
            "Auditoria",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                    "user_creacion",
                    "user_modificacion",
                    "active",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Si es nuevo
            obj.user_creacion = request.user
        obj.user_modificacion = request.user
        super().save_model(request, obj, form, change)
