from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
import math
from django.utils import timezone
from .models import TurnosModel


@receiver([post_save, post_delete], sender=TurnosModel)
def limpiar_cache_turnos(sender, **kwargs):
    hora = timezone.localtime().time()
    cache_key = f"turno_actual_{hora.hour}_{hora.minute // 30}"
    cache.delete(cache_key)
