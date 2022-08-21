from django.shortcuts import render, redirect
from products.models import Combination, ProductPrice, ProductType

# Create your views here.


def view_bag(request):
    """ A view that renders the bad contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product_types = request.POST.get('product_types')
    price = request.POST.get('product_price')
    redirect_url = request.POST.get('redirect_url')

    bag = request.session.get('bag', {})

    # if this product cobination does not exists, then create a new sub bag
    if not bag.get(item_id):
        bag[item_id] = {}

    bag[item_id][product_types] = True
    bag[item_id][price] = price

    print(price)
    request.session['bag'] = bag

    return redirect(redirect_url)
