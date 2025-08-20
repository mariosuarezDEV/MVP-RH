from django.contrib import admin
from unfold.admin import ModelAdmin

# Register your models here.
from .models import TurnosModel, PlantillaModel


@admin.register(TurnosModel)
class TurnosModelAdmin(ModelAdmin):
    list_display = ("id", "nombre", "hora_inicio", "hora_fin")
    search_fields = ("nombre",)
    ordering = ("hora_inicio",)
    readonly_fields = ("created_at", "updated_at", "user_creacion", "user_modificacion")
    fieldsets = (
        ("Información", {"fields": ("nombre", "hora_inicio", "hora_fin")}),
        (
            "Auditoría",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                    "user_creacion",
                    "user_modificacion",
                )
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Si es nuevo
            obj.user_creacion = request.user
        obj.user_modificacion = request.user
        super().save_model(request, obj, form, change)


@admin.register(PlantillaModel)
class PlantillaModelAdmin(ModelAdmin):
    list_display = ("id", "sucursal", "dia", "turno")
    search_fields = ("sucursal__nombre", "dia", "turno__nombre")
    ordering = ("dia", "turno")
    filter_horizontal = ("empleados",)
    readonly_fields = ("created_at", "updated_at", "user_creacion", "user_modificacion")
    fieldsets = (
        ("Información", {"fields": ("sucursal", "dia", "turno", "empleados")}),
        (
            "Auditoría",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                    "user_creacion",
                    "user_modificacion",
                )
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Si es nuevo
            obj.user_creacion = request.user
        obj.user_modificacion = request.user
        super().save_model(request, obj, form, change)
