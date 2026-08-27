from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    AssistantChatView,
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


urlpatterns = [
    path("assistant/", AssistantChatView.as_view(), name="assistant-chat"),
] + router.urls
