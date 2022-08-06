from django.db import models


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categroies"

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class ProductPrice(models.Model):
    product_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return str(self.product_price)


class ProductType(models.Model):
    ProductTypes = (
        ("STANDARD", "standard"),
        ("PANORAMIC", "panoramic"),
        ("3PANEL", "3panel"),
        ("5PANEL", "5panel"),
    )

    product_type = models.CharField(
        choices=ProductTypes, max_length=254, null=True, blank=True
    )
    product_price = models.ForeignKey(ProductPrice, on_delete=models.CASCADE)
    type_image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.product_type


class Combination(models.Model):
    option = models.ForeignKey(
        ProductType, null=False, blank=False, on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL
    )
    sku = models.CharField(max_length=254, null=False, blank=False)
    name = models.CharField(max_length=254)
    size = models.CharField(max_length=254)
    description = models.TextField()
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    colour = models.CharField(max_length=254)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    sku = models.CharField(
        max_length=254, null=False, blank=False)
    image = models.ImageField(null=True, blank=True)
