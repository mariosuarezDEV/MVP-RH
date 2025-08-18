from django_unicorn.components import UnicornView
from django.contrib.auth import get_user_model
from incidencias.models import BitacoraModel

User = get_user_model()


class IncidenciasEmpleadoView(UnicornView):
    usuario_id: int = None
    incidencias = []
    limite: int | None = None

    def mount(self):
        qs = BitacoraModel.objects.filter(usuario_id=self.usuario_id)
        if self.limite:
            qs = qs[: self.limite]
        self.incidencias = qs
