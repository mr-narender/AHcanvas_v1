from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404, redirect, render, reverse

from products.models import Category, Combination, Product
from .forms import ProductForm
from products.utils import paginateProducts


def all_products(request, page=1):
    """A view to show all products, including sorting and search queries"""

    products = Combination.objects.values_list(
        "sku", "name", "size", "rating", "colour"
    )
    products = Combination.objects.all()
    query = None
    categories = None
    size = None
    colour = None
    sort = None
    direction = None

    if request.GET:

        if "colour" in request.GET:
            colour = request.GET["colour"].split(",")
            products = products.filter(colour__in=colour)

        if "size" in request.GET:
            size = request.GET["size"].split(",")
            products = products.filter(size__in=size)

        if "category" in request.GET:
            categories = request.GET["category"].split(",")
            products = products.filter(category__name__in=categories)

        if "q" in request.GET:
            query = request.GET["q"]
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse("products"))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

        if "sort" in request.GET:
            sortkey = request.GET["sort"]
            sort = sortkey
            if sortkey == "name":
                sortkey = "lower_name"
                products = products.annotate(lower_name=Lower("name"))
            if sortkey == "category":
                sortkey = "category__name"
            if "direction" in request.GET:
                direction = request.GET["direction"]
                if direction == "desc":
                    sortkey = f"-{sortkey}"
            products = products.order_by(sortkey)

    current_sorting = f"{sort}_{direction}"

    custom_range, products = paginateProducts(request, products, 12)

    context = {
        "products": products,
        "search_term": query,
        "current_categories": categories,
        "current_size": size,
        "current_colour": colour,
        "current_sorting": current_sorting,
        "custom_range": custom_range,
    }
    print(context)
    return render(request, "products/products.html", context)


def product_detail(request, product_sku):
    """A view to show individual product details"""

    product = get_object_or_404(Product, sku=product_sku)
    product_combination = Combination.objects.filter(sku=product.sku)

    context = {
        "product_id": product_combination[0].id,
        "product": product,
        "products": product_combination,
        "name": product_combination[0].name,
        "rating": product_combination[0].rating,
        "description": product_combination[0].description,
        "category": product_combination[0].category,
        "size": product_combination[0].size,
    }

    return render(request, "products/product_detail.html", context)


def add_product(request):
    """ Add a product to the store """
    form = ProductForm()
    template = 'products/add_products.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
