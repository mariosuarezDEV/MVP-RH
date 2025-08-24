from django import forms
from .models import PuestosModel


class PuestosForm(forms.ModelForm):
    class Meta:
        model = PuestosModel
        fields = ["nombre", "descripcion"]
