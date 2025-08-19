from django import forms
from .models import BitacoraModel
from salarios.models import SalarioModel


class NuevaIncidenciaForm(forms.ModelForm):
    # los salarios mostrar solo los que tienen un puesto asociado
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["salario"].queryset = SalarioModel.objects.filter(
            puesto_asociado__isnull=False
        )

    class Meta:
        model = BitacoraModel
        fields = [
            "incidencia",
            "nota",
            "fecha_incidencia",
            "cubre_puesto",
            "salario",
        ]
        # widgets
        widgets = {
            "nota": forms.Textarea(attrs={"class": "form-control"}),
            "fecha_incidencia": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
            ),
            "cubre_puesto": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
