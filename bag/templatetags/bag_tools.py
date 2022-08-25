from django import template


register = template.Library()


@register.filter(name='calc_subtotal')
def calc_subtotal(product_price: int, quantity: int) -> float:
    return product_price * quantity

