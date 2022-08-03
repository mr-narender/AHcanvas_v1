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


class ProductPriceAdmin(admin.ModelAdmin):
    list_display = (
        'product_price',
    )


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = (
        'product_type',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(ProductPrice, ProductPriceAdmin)
