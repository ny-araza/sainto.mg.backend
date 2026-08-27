from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class ProduitMado(models.Model):
    name = models.CharField(max_length=255)

    price = models.DecimalField(max_digits=12, decimal_places=2)

    path = models.ImageField(upload_to="produits/", null=True, blank=True)

    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    nb_unite_in_pack = models.PositiveIntegerField(null=True, blank=True)

    is_unite = models.BooleanField(default=False)

    poid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "produit_mado"


class Client(models.Model):
    email = models.EmailField()

    date = models.DateTimeField(auto_now_add=True)

    message = models.TextField(blank=True, null=True)

    rating = models.PositiveSmallIntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self):
        return self.email

    class Meta:
        db_table = "client"


class ProduitLike(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="likes")

    produit = models.ForeignKey(
        ProduitMado, on_delete=models.CASCADE, related_name="likes"
    )

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "produit_like"

        # Empêche un client de liker deux fois
        # le même produit
        constraints = [
            models.UniqueConstraint(
                fields=["client", "produit"], name="unique_client_produit_like"
            )
        ]

    def __str__(self):
        return f"{self.client.email} aime {self.produit.name}"


class Pub(models.Model):
    path = models.ImageField(upload_to="pub/")

    class Meta:
        db_table = "pub"

    def __str__(self):
        return f"Publicité {self.id}"
