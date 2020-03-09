from django import template

register = template.Library()


@register.filter("replace_comma_and")
def replace_comma_and(value):
    return value.replace(",", " and")
