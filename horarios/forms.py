from django import forms
from .models import PlantillaModel
from django.contrib.auth import get_user_model
from sucursales.models import SucursalModel
from django.db import connection

User = get_user_model()


class PlantillaForm(forms.ModelForm):
    # Constructor
    def __init__(self, *args, **kwargs):
        # Extraer la sucursal del kwargs
        self.sucursal = kwargs.pop("sucursal", None)
        # recibe el id de la sucursal
        # IMPORTANTE: Llamar a super() ANTES de acceder a self.fields
        super().__init__(*args, **kwargs)
        if self.sucursal:
            # Filtrar los empleados por la sucursal proporcionada
            self.fields["empleados"].queryset = User.objects.filter(
                sucursal_id=self.sucursal
            ).select_related("sucursal", "puesto", "salario")
        else:
            self.fields["empleados"].queryset = User.objects.none()  # Sin empleados

    empleados = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),  # Queryset inicial vacío
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = PlantillaModel
        fields = ["dia", "turno", "empleados"]
        # widgets
        widgets = {
            "dia": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
            ),
        }


# Wizar de formularios


class DiaTurnoForm(forms.ModelForm):
    class Meta:
        model = PlantillaModel
        fields = ["dia", "turno"]
        widgets = {
            "turno": forms.Select(attrs={"class": "form-control"}),
            "dia": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
            ),
        }


class EmpleadosSucursalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # Extraer la sucursal del kwargs
        self.sucursal = kwargs.pop("sucursal", None)
        # recibe el id de la sucursal
        # IMPORTANTE: Llamar a super() ANTES de acceder a self.fields
        super().__init__(*args, **kwargs)
        if self.sucursal:
            # Filtrar los empleados por la sucursal proporcionada
            self.fields["empleados"].queryset = User.objects.filter(
                sucursal_id=self.sucursal
            ).select_related("sucursal", "puesto", "salario")

    empleados = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),  # Queryset inicial vacío
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = PlantillaModel
        fields = ["empleados"]


class OtrosEmpleadosForm(forms.Form):
    otros_empleados = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        # Extraer la sucursal del kwargs
        self.sucursal = kwargs.pop("sucursal", None)
        super().__init__(*args, **kwargs)
        if self.sucursal:
            # Excluir los empleados de la sucursal y los que no tengan sucursal
            self.fields["otros_empleados"].queryset = (
                User.objects.exclude(sucursal_id=self.sucursal)
                .filter(sucursal__isnull=False)
                .select_related("sucursal", "puesto", "salario")
            )
