from unfold.admin import ModelAdmin
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin

# Register your models here.
from .models import User
from django.contrib.auth.models import Group

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "username",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        # Agregar campos si es necesario
    )
    search_fields = (
        "first_name",
        "last_name",
        "username",
        "email",
    )
    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
    )
    list_editable = (
        "is_active",
        "is_staff",
        "is_superuser",
    )
    fieldsets = (
        (
            "Datos Personales",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "email",
                    # Agregar campos si es necesario
                ),
                "classes": ("wide",),
            },
        ),
        (
            "Recursos Humanos",
            {
                "fields": ("puesto", "salario", "fecha_ingreso", "sucursal"),
                "classes": ("wide",),
            },
        ),
        (
            "Permisos",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
                "classes": ("wide",),
            },
        ),
        ("Asignación de grupos", {"fields": ("groups",), "classes": ("collapse",)}),
        (
            "Auditoria",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                ),
                "classes": ("wide",),
            },
        ),
        (
            "Seguridad",
            {
                "fields": (
                    "user_permissions",
                    # Contraseña
                    "password",
                ),
                "classes": ("wide",),
            },
        ),
    )


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
