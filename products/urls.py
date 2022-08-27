from django.urls import path, re_path

from products import views

urlpatterns = [
    path("add/", views.add_product, name="add_product"),
    path("int:detail/<product_sku>/", views.product_detail, name="product_detail"),
    re_path(r"^(page/(?P<page>\d+))?/$/", views.all_products, name="products"),
    path(r"", views.all_products, name="products"),
]
