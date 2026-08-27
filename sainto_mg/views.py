from django.db.models import Avg
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Client, ProduitLike, ProduitMado
from .serializers import (
    ClientSerializer,
    ProduitLikeDetailSerializer,
    ProduitLikeSerializer,
    ProduitMadoSerializer,
)

# =========================================================
# PRODUITS
# =========================================================


class ProduitMadoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/produits/
    GET /api/produits/{id}/
    """

    queryset = ProduitMado.objects.all()
    serializer_class = ProduitMadoSerializer


# =========================================================
# CLIENT
# =========================================================


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def create(self, request, *args, **kwargs):

        email = request.data.get("email")

        if not email:
            return Response(
                {"status": False, "message": "L'email est obligatoire"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        client, created = Client.objects.get_or_create(
            email=email,
            defaults={
                "message": request.data.get("message"),
                "rating": request.data.get("rating"),
            },
        )

        # Si le client existe déjà et qu'un feedback
        # est envoyé, on peut mettre à jour son feedback.
        if not created:
            message = request.data.get("message")
            rating = request.data.get("rating")

            if message is not None:
                client.message = message

            if rating is not None:
                client.rating = rating

            client.save()

        serializer = self.get_serializer(client)

        return Response(
            {
                "status": True,
                "created": created,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# =========================================================
# LIKES
# =========================================================


class ProduitLikeViewSet(viewsets.ModelViewSet):
    """
    POST   /api/likes/
    DELETE /api/likes/{id}/
    """

    queryset = ProduitLike.objects.select_related("client", "produit").all()

    serializer_class = ProduitLikeSerializer

    http_method_names = [
        "get",
        "post",
        "delete",
        "head",
        "options",
    ]

    def create(self, request, *args, **kwargs):
        """
        Empêche un client de liker
        plusieurs fois le même produit.
        """

        client_id = request.data.get("client")
        produit_id = request.data.get("produit")

        if not client_id or not produit_id:
            return Response(
                {"status": False, "message": "client et produit sont obligatoires"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Vérifie si le like existe déjà
        if ProduitLike.objects.filter(
            client_id=client_id, produit_id=produit_id
        ).exists():
            return Response(
                {"status": False, "message": "Ce client a déjà liké ce produit"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response(
            {
                "status": True,
                "message": "Produit liké avec succès",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class ProduitMadoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProduitMado.objects.all()
    serializer_class = ProduitMadoSerializer

    @action(detail=True, methods=["get"], url_path="ratings")
    def ratings(self, request, pk=None):

        produit = self.get_object()

        clients = Client.objects.filter(likes__produit=produit, rating__isnull=False)

        moyenne = clients.aggregate(moyenne=Avg("rating"))["moyenne"]

        total = clients.count()

        return Response(
            {
                "status": True,
                "product": produit.id,
                "total": total,
                "average": round(float(moyenne), 2) if moyenne else 0,
            }
        )
