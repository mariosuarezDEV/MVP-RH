from django_unicorn.components import UnicornView
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class BuscardorView(UnicornView):
    nombre = ""
    mostrar_resultados = False
    empleados = []

    def buscar(self):
        self.mostrar_resultados = True
        if self.nombre != "":
            self.empleados = User.objects.filter(
                Q(first_name__icontains=self.nombre)
                | Q(last_name__icontains=self.nombre)
                | Q(username__icontains=self.nombre)
            )[:5]
        else:
            self.mostrar_resultados = False
            self.empleados = []
