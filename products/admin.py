from django.contrib import admin
from .models import Product, Category, ProductType, ProductPrice

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'size',
        'colour',
    )

    ordering = ('sku',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(ProductType)
admin.site.register(ProductPrice)
