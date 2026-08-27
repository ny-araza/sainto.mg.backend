from rest_framework.routers import DefaultRouter

from .views import (
    ClientViewSet,
    ProduitLikeViewSet,
    ProduitMadoViewSet,
    PubViewSet,
)

router = DefaultRouter()

router.register(r"produits", ProduitMadoViewSet, basename="produits")

router.register(r"clients", ClientViewSet, basename="clients")

router.register(r"likes", ProduitLikeViewSet, basename="likes")

router.register("pubs", PubViewSet, basename="pub")
urlpatterns = router.urls
