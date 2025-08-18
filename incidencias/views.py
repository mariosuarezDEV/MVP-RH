# vistas
from django.views.generic import CreateView

# Modelos
from .models import BitacoraModel

# Formularios
from .forms import BitacoraForm

# Mixins
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.
