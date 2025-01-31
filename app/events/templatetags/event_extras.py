from django import template

register = template.Library()

@register.filter
def not_archived(value):
    """ Extra template tag filter to not display archived events """
    return value.filter(is_archived=False)