from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.contrib import messages

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
        bag[f"{combination.id}"] += quantity
        messages.success(request, f'Updated {combination.name} quantity to {bag[item_id]}')
    else:
        bag[f"{combination.id}"] = quantity
        messages.success(request, f'Added {combination.name} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ Adjust the quantity of the specified product to the specified amount """

    product_types = request.POST.get('product_types')
    quantity = int(request.POST.get('quantity'))
    option = 0
    if product_types == 'STANDARD':
        option = 1
    elif product_types == 'PANORAMIC':
        option = 2
    elif product_types == '3PANEL':
        option = 3
    elif product_types == '5PANEL':
        option = 4

    combination = get_object_or_404(Combination, pk=item_id)
    bag = request.session.get('bag', {})

    if quantity > 0:
        bag[f"{combination.id}"] = quantity
        messages.success(request, f'Updated {combination.name} quantity to {bag[item_id]}')
    else:
        if quantity > 0:
            bag[f"{combination.id}"] = quantity
            messages.success(request, f'Updated {combination.name} quantity to {bag[item_id]}')
        else:
            bag.pop(f"{combination.id}")
            messages.success(request, f'Removed {combination.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """ Remove the item from the shopping bag """

    product_types = request.POST.get('product_types')
    quantity = int(request.POST.get('quantity', 0))
    option = 0
    if product_types == 'STANDARD':
        option = 1
    elif product_types == 'PANORAMIC':
        option = 2
    elif product_types == '3PANEL':
        option = 3
    elif product_types == '5PANEL':
        option = 4

    combination = get_object_or_404(Combination, pk=item_id)
    bag = request.session.get('bag', {})

    try:

        bag.pop(f"{combination.id}")
        messages.success(request, f'Removed {combination.name} from your bag')

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
