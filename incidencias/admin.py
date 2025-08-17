from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import TipoIncidenciaModel, IncidenciasModel, BitacoraModel


# Register your models here.


@admin.register(TipoIncidenciaModel)
class TipoIncidenciaAdmin(ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)
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


@admin.register(IncidenciasModel)
class IncidenciasAdmin(ModelAdmin):
    list_display = ("tipo", "prompt")
    search_fields = ("tipo__nombre", "prompt")
    readonly_fields = ("created_at", "updated_at", "user_creacion", "user_modificacion")
    fieldsets = (
        (
            "Información",
            {"fields": ("tipo", "nombre", "prompt")},
        ),
        (
            "Auditoria",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                    "user_creacion",
                    "user_modificacion",
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


@admin.register(BitacoraModel)
class BitacoraAdmin(ModelAdmin):
    list_display = ("usuario", "incidencia", "monto", "estado", "fecha_incidencia")
    search_fields = ("usuario__username", "incidencia__nombre", "estado")
    readonly_fields = ("created_at", "updated_at", "user_creacion", "user_modificacion")
    autocomplete_fields = ("usuario", "incidencia")
    fieldsets = (
        (
            "Información",
            {
                "fields": (
                    "usuario",
                    "incidencia",
                    "cubre_puesto",
                    "salario",
                    "nota",
                    "monto",
                    "fecha_incidencia",
                    "estado",
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
