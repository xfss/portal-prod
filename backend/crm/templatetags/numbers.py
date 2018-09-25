from django import template
from django.template.defaultfilters import floatformat
from django.utils.html import mark_safe

register = template.Library()


@register.filter
def currency(amount, currency='CHF'):
    try:
        return mark_safe("{:0,.2f}&nbsp;{}".format(float(amount), currency).replace(',', "'").strip())
    except (ValueError, TypeError):
        return "-"


@register.filter
def number(n):
    try:
        return "{:0,d}".format(int(n)).replace(',', "'")
    except (ValueError, TypeError):
        return "-"


@register.filter
def percentage(n, format=2):
    try:
        return floatformat(float(n)*100, format) + "%"
    except (ValueError, TypeError):
        return "-"
