from django import template

register = template.Library()


@register.filter
def normalize_title(string, char="-"):
    return string.replace(char, " ")
