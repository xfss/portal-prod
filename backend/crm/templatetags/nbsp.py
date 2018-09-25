from django import template
from django.utils.html import mark_safe

register = template.Library()


@register.filter
def nbsp(text: str):
    return mark_safe(text.replace(" ", "&nbsp;"))
