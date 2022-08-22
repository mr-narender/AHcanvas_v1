from django.shortcuts import render, redirect
from products.models import Combination, ProductPrice, ProductType

# Create your views here.


def view_bag(request):
    """ A view that renders the bad contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product_types = request.POST.get('product_types')
    sku = request.POST.get('sku')
    price = request.POST.get('product_price')
    redirect_url = request.POST.get('redirect_url')
    print('--startofpostrequest')
    print(request.POST)
    print(f'sku = {sku}')
    print(f'product_types = {product_types}')
    print(f'price = {price}')
    option = 0
    if product_types == 'STANDARD':
        option = 1
    elif product_types == 'PANORAMIC':
        option = 2
    elif product_types == '3PANEL':
        option = 3
    elif product_types == '5PANEL':
        option = 4

    combination = Combination.objects.filter(sku=sku).filter(option=option)
    combination = combination[0]
    bag = request.session.get('bag', {})

    # if this product cobination does not exists, then create a new sub bag
    # if not bag.get(item_id):
    #     bag[item_id] = {}

    # bag[item_id][product_types] = True
    # bag[item_id][price] = price
    if str(combination.id) in list(bag.keys()):
        # if quantity += quauntity
        bag[str(combination.id)] += 1
    else:
        bag[combination.id] = 1

    request.session['bag'] = bag
    print(request.session['bag'])

    return redirect(redirect_url)
