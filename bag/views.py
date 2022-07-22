from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


def view_bag(request):
    """ A view that renders the bad contents page """

    return render(request, 'bag/bag.html')
