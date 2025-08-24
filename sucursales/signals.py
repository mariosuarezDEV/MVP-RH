from django.db.models.signals import post_save, post_delete
from .models import SucursalModel
from django.dispatch import receiver
from django.core.cache import cache


@receiver([post_save, post_delete], sender=SucursalModel)
def clear_sucursales_cache(sender, **kwargs):
    cache.delete("sucursales")
