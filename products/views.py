from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404, redirect, render, reverse

from products.models import Category, Combination, Product
from .forms import ProductForm, CombinationForm, DeleteForm
from products.utils import paginateProducts


def all_products(request, page=1):
    """A view to show all products, including sorting and search queries"""

    products = Combination.objects.values_list(
        "sku", "name", "size", "rating", "colour",
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
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse("products"))

            queries = Q(name__icontains=query) | Q(
                description__icontains=query)
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
        "image": product_combination[0].image,
        "option": product_combination[0].option
    }

    print(context)
    return render(request, "products/product_detail.html", context)


def add_product(request):
    """ Add a product to the store """

    if request.method == 'POST':
        form_product = ProductForm(request.POST, request.FILES)
        if form_product.is_valid():
            form_product.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('products'))
        else:
            messages.error(
                request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form_product = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form_product,
    }

    return render(request, template, context)


def add_combination(request):
    """ Add a combination to the store """

    if request.method == 'POST':
        form_combination = CombinationForm(request.POST, request.FILES)
        if form_combination.is_valid():
            combination = form_combination.save()
            messages.success(request, 'Successfully added combination!')
            return redirect(reverse('product_detail', args=[combination.sku]))
        else:
            messages.error(
                request, 'Failed to add combination. Please ensure the form is valid.')
    else:
        form_combination = CombinationForm()

    template = 'products/add_combination.html'
    context = {
        'form': form_combination,
    }

    return render(request, template, context)


def edit_product(request, product_sku):
    """ Edit a product in the store """

    product = get_object_or_404(Product, sku=product_sku)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.sku]))
        else:
            messages.error(
                request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form_product = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.sku}')

    template = 'products/edit_product.html'
    context = {
        'form': form_product,
        'product': product,
    }

    return render(request, template, context)


def edit_combination(request, product_sku, pk):
    """ Edit a combination in the store """

    combination = Combination.objects.get(sku=product_sku, pk=pk)
    product_combination = Combination.objects.filter(sku=product_sku)
    product = Product.objects.get(sku=product_sku)
    if request.method == 'POST':
        form = CombinationForm(
            request.POST, request.FILES, instance=combination)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.sku]))
        else:
            messages.error(
                request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form_combination = CombinationForm(instance=combination)
        messages.info(request, f'You are editing {combination.sku}')

    template = 'products/edit_combination.html'
    context = {
        'form': form_combination,
        "product_id": pk,
        "product": product,
        "products": product_combination,
        'combination': combination,
    }

    return render(request, template, context)


def delete_product(request, product_sku):
    """ Delete a product from the store """
    product = get_object_or_404(Product, sku=product_sku)
    product_combination = Combination.objects.filter(sku=product.sku)
    for item in product_combination:
        item.delete()
    product.delete()
    messages.success(request, 'Product deleted!')

    return redirect(reverse('products'))
