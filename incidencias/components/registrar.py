from django_unicorn.components import UnicornView
from incidencias.models import IncidenciasModel
from salarios.models import SalarioModel


class RegistrarView(UnicornView):
    incidencias = IncidenciasModel.objects.all()
    nota = ""
    fecha_incidencia = ""
    cubre_puesto: bool = False
    puesto_objetivo = SalarioModel.objects.all()
