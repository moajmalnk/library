from django import template

register = template.Library()


@register.filter
def make_positive(value):
    return abs(value)


@register.filter
def subtract(value, arg):
    return value - arg


@register.filter
def sum_attribute(value, arg):
    return value + arg
