from django.db.models.signals import post_save, post_delete
from .models import EmpresaModel
from django.dispatch import receiver
from django.core.cache import cache


@receiver([post_save, post_delete], sender=EmpresaModel)
def clear_empresas_cache(sender, **kwargs):
    cache.delete("empresas")  # si usas django-redis
