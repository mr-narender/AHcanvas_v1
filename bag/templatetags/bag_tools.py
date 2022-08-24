from django import template


register = template.Library()


@register.filter(name='calc_subtotal')
def calc_subtotal(product_price, quantity):
    return int('product_price') * quantity

