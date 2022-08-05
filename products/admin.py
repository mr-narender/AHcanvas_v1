from django.contrib import admin

from products.models import Category, Combination, Product, ProductPrice, ProductType

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku",)

    ordering = ("sku",)


class CombinationAdmin(admin.ModelAdmin):
    list_display = (
        "option",
        "category",
        "sku",
        "name",
        "size",
        "description",
        "rating",
        "colour",
        "image",
    )

    ordering = ("sku",)


class ProductPriceAdmin(admin.ModelAdmin):
    list_display = ("product_price",)


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ("product_type",)


admin.site.register(Product, ProductAdmin)
admin.site.register(Combination, CombinationAdmin)
admin.site.register(Category)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(ProductPrice, ProductPriceAdmin)
