from django.contrib import admin

from .models import Client, ProduitLike, ProduitMado


@admin.register(ProduitMado)
class ProduitMadoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "rate",
        "path",
    )


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "date",
    )


@admin.register(ProduitLike)
class ProduitLikeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "client",
        "produit",
        "date",
    )
