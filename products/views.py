from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404, redirect, render, reverse

from products.models import Category, Product, ProductPrice, ProductType, Combination
from products.utils import paginateProducts


def all_products(request):
    """A view to show all products, including sorting and search queries"""

    products = Product.objects.all()
    products_info = Combination.objects.all()
    custom_range, products = paginateProducts(request, products, 12)
    
    context = {
        'products': products,
        "products_info": products_info
    }

    return render(request, "products/products.html", context)


def product_detail(request, product_id):
    """A view to show individual product details"""

    product = get_object_or_404(Product, pk=product_id)
    product_type = ProductType.objects.all()
    product_price = ProductPrice.objects.all()

    context = {
        "product": product,
        "product_type": product_type,
        "product_price": product_price,
    }

    return render(request, "products/product_detail.html", context)