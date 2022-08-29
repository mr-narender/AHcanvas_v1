from django.shortcuts import get_object_or_404
from products.models import Combination


def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get("bag", {})

    for item_id, quantity in bag.items():
        combination = get_object_or_404(Combination, pk=item_id)
        total += quantity * combination.option.product_price.product_price
        product_count += quantity
        bag_items.append(
            {
                "item_id": item_id,
                "quantity": quantity,
                "combination": combination,
            }
        )

    context = {
        "bag_items": bag_items,
        "total": total,
        "product_count": product_count,
    }

    return context
