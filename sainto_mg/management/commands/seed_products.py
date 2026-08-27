from django.core.management.base import BaseCommand

from sainto_mg.models import ProduitMado


class Command(BaseCommand):
    help = "Insère les produits SAINTO et ICE TEA"

    def handle(self, *args, **kwargs):

        produits = [
            {
                "id": 1,
                "name": "SAINTO 1.5L",
                "price": 2291.66,
                "rate": 4.8,
                "path": "#",
                "nb_unite_in_pack": 6,
                "poid": 9,
                "is_unite": False,
            },
            {
                "id": 2,
                "name": "SAINTO 1L",
                "price": 1388.33,
                "rate": 4.7,
                "path": "#",
                "nb_unite_in_pack": 6,
                "poid": 6,
                "is_unite": False,
            },
            {
                "id": 3,
                "name": "SAINTO 0.5L",
                "price": 1180,
                "rate": 4.6,
                "path": "#",
                "nb_unite_in_pack": 8,
                "poid": 4,
                "is_unite": False,
            },
            {
                "id": 4,
                "name": "SAINTO 5L",
                "price": 4166.66,
                "rate": 4.9,
                "path": "#",
                "nb_unite_in_pack": None,
                "is_unite": True,
                "poid": 5,
            },
            {
                "id": 5,
                "name": "Bonbonne 1ère Livraison",
                "price": 73333.33,
                "rate": 4.5,
                "path": "#",
                "nb_unite_in_pack": None,
                "is_unite": True,
                "poid": 20,
            },
            {
                "id": 6,
                "name": "Bonbonne Recharge",
                "price": 30000,
                "rate": 4.8,
                "path": "#",
                "nb_unite_in_pack": None,
                "is_unite": True,
                "poid": 9,
            },
            {
                "id": 7,
                "name": "ICE TEA pomme 1.5L",
                "price": 6805,
                "rate": 4.7,
                "path": "#",
                "nb_unite_in_pack": 6,
                "is_unite": False,
                "poid": 9,
            },
            {
                "id": 8,
                "name": "ICE TEA pêche 1.5L",
                "price": 6805,
                "rate": 4.9,
                "path": "#",
                "nb_unite_in_pack": 6,
                "is_unite": False,
                "poid": 9,
            },
            {
                "id": 9,
                "name": "ICE TEA citron 1.5L",
                "price": 6805,
                "rate": 4.6,
                "path": "#",
                "nb_unite_in_pack": 6,
                "is_unite": False,
                "poid": 9,
            },
            {
                "id": 10,
                "name": "ICE TEA pomme 0.5L",
                "price": 2916.66,
                "rate": 4.5,
                "path": "#",
                "nb_unite_in_pack": 8,
                "is_unite": False,
                "poid": 4,
            },
            {
                "id": 11,
                "name": "ICE TEA pêche 0.5L",
                "price": 2916.66,
                "rate": 4.8,
                "path": "#",
                "nb_unite_in_pack": 8,
                "is_unite": False,
                "poid": 4,
            },
            {
                "id": 12,
                "name": "ICE TEA citron 0.5L",
                "price": 2916.66,
                "rate": 4.7,
                "path": "#",
                "nb_unite_in_pack": 8,
                "is_unite": False,
                "poid": 4,
            },
        ]

        for produit in produits:
            produit_id = produit.pop("id")

            ProduitMado.objects.update_or_create(id=produit_id, defaults=produit)

        self.stdout.write(
            self.style.SUCCESS("Tous les produits ont été insérés avec succès !")
        )
