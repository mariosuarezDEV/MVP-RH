from django import forms
from .models import SucursalModel


class SucursalForm(forms.ModelForm):
    class Meta:
        model = SucursalModel
        fields = ["empresa", "nombre"]
