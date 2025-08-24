from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import PuestosModel
from django.core.cache import cache


@receiver([post_save, post_delete], sender=PuestosModel)
def clear_cache_on_save(sender, instance, **kwargs):
    cache.delete("puestos")
