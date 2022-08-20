from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product, Combination, ProductType, ProductPrice


def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for item_id, quantity in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        all_prodcuts_for_purchase = Combination.objects.filter(
            sku=product.sku).filter(option__in=ProductType.objects.filter(
                product_type__in=quantity))

        #total = Combination.option.product_price.product_price
        bag_items.append({
            'item_id': item_id,
            'product': product,
        })

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
    }

    return context
