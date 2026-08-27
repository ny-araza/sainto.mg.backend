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
    """
    POST /api/clients/
    GET /api/clients/
    GET /api/clients/{id}/
    """

    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    @action(detail=True, methods=["get"], url_path="likes")
    def likes(self, request, pk=None):
        """
        GET /api/clients/{id}/likes/
        """

        client = self.get_object()

        likes = client.likes.select_related("produit").all()

        serializer = ProduitLikeDetailSerializer(likes, many=True)

        return Response(
            {
                "status": True,
                "client": client.id,
                "total_likes": likes.count(),
                "data": serializer.data,
            }
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
