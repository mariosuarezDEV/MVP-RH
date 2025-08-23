from django import forms
from .models import EmpresaModel


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = EmpresaModel
        fields = ["nombre"]
