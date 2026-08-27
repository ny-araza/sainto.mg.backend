from rest_framework import serializers

from .models import Client, ProduitLike, ProduitMado, Pub


class ProduitMadoSerializer(serializers.ModelSerializer):
    path = serializers.SerializerMethodField()
    rate = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()

    class Meta:
        model = ProduitMado

        fields = [
            "id",
            "name",
            "price",
            "path",
            "rate",
            "total_likes",
            "nb_unite_in_pack",
            "is_unite",
            "poid",
        ]

    def get_path(self, obj):
        request = self.context.get("request")

        if not obj.path:
            return None

        if request:
            return request.build_absolute_uri(obj.path.url)

        return obj.path.url

    def get_total_likes(self, obj):
        return obj.likes.count()

    def get_rate(self, obj):
        # Nombre de likes du produit actuel
        likes_produit = obj.likes.count()

        # Chercher le produit qui possède le plus de likes
        produits = ProduitMado.objects.all()

        max_likes = max([produit.likes.count() for produit in produits], default=0)

        # Aucun like dans toute la base
        if max_likes == 0:
            return 1.0

        # Conversion sur une échelle de 1 à 5
        rate = 1 + (likes_produit / max_likes) * 4

        return round(rate, 1)


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "id",
            "email",
            "date",
            "message",
        ]

        read_only_fields = [
            "id",
            "date",
        ]


class ProduitLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProduitLike
        fields = [
            "id",
            "client",
            "produit",
            "date",
        ]

        read_only_fields = [
            "id",
            "date",
        ]


class ProduitLikeDetailSerializer(serializers.ModelSerializer):
    produit = ProduitMadoSerializer(read_only=True)

    class Meta:
        model = ProduitLike
        fields = [
            "id",
            "produit",
            "date",
        ]


class PubSerializer(serializers.ModelSerializer):
    path = serializers.SerializerMethodField()

    class Meta:
        model = Pub

        fields = [
            "id",
            "path",
        ]

    def get_path(self, obj):
        request = self.context.get("request")

        if not obj.path:
            return None

        if request:
            return request.build_absolute_uri(obj.path.url)

        return obj.path.url
