from django.shortcuts import render, redirect

# Create your views here.


def view_bag(request):
    """ A view that renders the bad contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    redirect_url = request.POST.get('redirect_url')
    product_types = request.POST.get('product_types')

    bag = request.session.get('bag', {})

    bag[item_id] = product_types

    request.session['bag'] = bag
    return redirect(redirect_url)
