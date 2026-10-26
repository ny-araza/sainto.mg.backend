from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    AssistantChatView,
    ClientViewSet,
    ProduitLikeViewSet,
    ProduitMadoViewSet,
    PubViewSet,
    send_devis_email
)

router = DefaultRouter()

router.register(r"produits", ProduitMadoViewSet, basename="produits")

router.register(r"clients", ClientViewSet, basename="clients")

router.register(r"likes", ProduitLikeViewSet, basename="likes")

router.register("pubs", PubViewSet, basename="pub")


urlpatterns = [
    path("assistant/", AssistantChatView.as_view(), name="assistant-chat"),
    path(
        "send-devis-email/",
        send_devis_email,
        name="send_devis_email",
    ),
] + router.urls
