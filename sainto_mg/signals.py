from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import ProduitMado
from .views import CACHE_KEY_PRODUITS  # ou déplace la constante dans un module partagé


@receiver([post_save, post_delete], sender=ProduitMado)
def invalidate_produits_cache(sender, **kwargs):
    cache.delete(CACHE_KEY_PRODUITS)
