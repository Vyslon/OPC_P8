from django.db import models
from django.contrib.auth.models import User


class Categories(models.Model):
    """
    Categories of product from OpenFoodFacts
    """
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Products(models.Model):
    """
    Products from OpenFoodFacts
    """
    name = models.CharField(max_length=100, unique=True)
    stores = models.CharField(max_length=100)
    nutrition_grade = models.CharField(max_length=1)
    url_openfoodfact = models.URLField(max_length=100)
    image_url = models.URLField(max_length=100, default="none")
    categories = models.ManyToManyField(Categories)

    def __str__(self):
        return self.name


class platform_user(models.Model):
    """
    For each user, it's a link between a substituted product (for which they
    asked for substitutes) and it's substitutes chosed by the user
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    substituted_product = models.ForeignKey(
        Products,
        related_name="produit_substitute",
        null=True,
        on_delete=models.SET_NULL)
    substituent_product = models.ForeignKey(
        Products,
        related_name="produit_substituant",
        on_delete=models.CASCADE)

    class Meta:
        """
        Unique index to have only 1 column substituted product/substiuent
        product for each user (so you can't save more than 1 time the same
        couple)
        """
        unique_together = ("user", "substituted_product", "substituent_product")
