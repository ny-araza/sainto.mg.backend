import requests
from django.core.cache import cache
from django.db.models import Avg
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Client, ProduitLike, ProduitMado, Pub
from .serializers import (
    ClientSerializer,
    ProduitLikeDetailSerializer,
    ProduitLikeSerializer,
    ProduitMadoSerializer,
    PubSerializer,
)

# =========================================================
# PRODUITS
# =========================================================
CACHE_KEY_PRODUITS = "assistant_produits_text"
CACHE_TIMEOUT = 60 * 15  # 15 minutes


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


def build_produits_text():
    """Construit le texte des produits à insérer dans le prompt."""
    produits_qs = (
        ProduitMado.objects.only("name", "price", "nb_unite_in_pack", "poid").order_by(
            "name"
        )[:100]  # limite pour ne pas exploser le prompt
    )

    if not produits_qs.exists():
        return "Aucun produit disponible actuellement."

    lignes = []
    for p in produits_qs:
        prix = f"{p.price:,.0f}".replace(",", " ")
        ligne = f"- {p.name} : {prix} Ar"
        if p.nb_unite_in_pack:
            ligne += f" (pack de {p.nb_unite_in_pack} unités)"
        if p.poid:
            ligne += f" - poids : {p.poid}"
        lignes.append(ligne)

    return "Produits disponibles :\n" + "\n".join(lignes)


def get_produits_text():
    """Récupère le texte des produits depuis le cache, ou le reconstruit."""
    produits_text = cache.get(CACHE_KEY_PRODUITS)
    if produits_text is None:
        produits_text = build_produits_text()
        cache.set(CACHE_KEY_PRODUITS, produits_text, CACHE_TIMEOUT)
    return produits_text


ROLES_AUTORISES = {"user", "assistant"}
MAX_HISTORIQUE = 20  # limite le nombre de messages envoyés au modèle


class AssistantChatView(APIView):
    def post(self, request):
        message = request.data.get("message")
        if not message:
            return Response({"error": "Le message est obligatoire"}, status=400)

        historique_brut = request.data.get("historique", [])
        if not isinstance(historique_brut, list):
            return Response(
                {"error": "Le format de l'historique est invalide"}, status=400
            )

        # Validation et nettoyage de l'historique reçu du frontend
        historique_valide = []
        for item in historique_brut[-MAX_HISTORIQUE:]:
            role = item.get("role")
            content = item.get("content")
            if role in ROLES_AUTORISES and isinstance(content, str) and content.strip():
                historique_valide.append({"role": role, "content": content})

        # Pas de message "system" ici : Ollama applique automatiquement
        # celui défini dans le Modelfile du modèle "assistant-vente"
        messages_ollama = historique_valide + [{"role": "user", "content": message}]

        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "assistant-vente",
                "stream": False,
                "messages": messages_ollama,
            },
        )
        data = response.json()
        return Response({"message": data["message"]["content"]})


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
            },
        )

        # Si le client existe déjà et qu'un feedback
        # est envoyé, on peut mettre à jour son feedback.
        if not created:
            message = request.data.get("message")

            if message is not None:
                client.message = message

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


class PubViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Pub.objects.all().order_by("-id")
    serializer_class = PubSerializer
