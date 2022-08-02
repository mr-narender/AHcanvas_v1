from django.db import models


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categroies'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    size = models.CharField(max_length=254)
    description = models.TextField()
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    colour = models.CharField(max_length=254)
    image = models.ImageField(null=True, blank=True)
    product_type = models.ForeignKey('ProductType', on_delete=models.CASCADE, max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name


class ProductType(models.Model):
    ProductTypes = (
        ('STANDARD', 'standard'),
        ('PANORAMIC', 'panoramic'),
        ('3PANEL', '3panel'),
        ('5PANEL', '5panel')
    )
    product_type = models.CharField(choices=ProductTypes, max_length=254, null=True, blank=True)
    product_price = models.ForeignKey('ProductPrice', on_delete=models.CASCADE)
    product_image = models.ImageField(null=True, blank=True)


class ProductPrice(models.Model):
    product_price = models.DecimalField(max_digits=6, decimal_places=2)
