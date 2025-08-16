from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import PuestosModel

# Register your models here.


@admin.register(PuestosModel)
class PuestosAdmin(ModelAdmin):
    list_display = ("nombre", "descripcion")
    search_fields = ("nombre", "descripcion")
    readonly_fields = (
        "user_creacion",
        "user_modificacion",
        "created_at",
        "updated_at",
    )
    fieldsets = (
        ("Información", {"fields": ("nombre", "descripcion")}),
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
