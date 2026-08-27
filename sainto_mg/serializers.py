from rest_framework import serializers

from .models import Client, ProduitLike, ProduitMado


class ProduitMadoSerializer(serializers.ModelSerializer):
    path = serializers.SerializerMethodField()

    class Meta:
        model = ProduitMado

        fields = [
            "id",
            "name",
            "price",
            "path",
            "rate",
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
