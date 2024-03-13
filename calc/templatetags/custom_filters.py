from django import template

register = template.Library()


@register.filter(name='add_commas')
def add_commas(value):
    try:
        value = int(value)
        return "{:,}".format(value)
    except (TypeError, ValueError):
        return value
