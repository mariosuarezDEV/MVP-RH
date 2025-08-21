from django import forms
from django.contrib.auth import get_user_model
from martor.fields import MartorFormField

User = get_user_model()


class BiografiaForm(forms.ModelForm):
    biografia = MartorFormField()

    class Meta:
        model = User
        fields = ["biografia"]
