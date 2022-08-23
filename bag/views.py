from django.shortcuts import render, redirect
from products.models import Combination

# Create your views here.


def view_bag(request):
    """ A view that renders the bad contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product_types = request.POST.get('product_types')
    quantity = int(request.POST.get('quantity'))
    sku = request.POST.get('sku')
    price = request.POST.get('product_price')
    redirect_url = request.POST.get('redirect_url')
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

    if str(combination.id) in list(bag.keys()):
        bag[str(combination.id)] += quantity
    else:
        bag[combination.id] = quantity

    request.session['bag'] = bag
    print(request.session['bag'])

    return redirect(redirect_url)
