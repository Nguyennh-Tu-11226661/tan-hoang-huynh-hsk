from django import template


register = template.Library()


@register.filter
def vnd(value):
    try:
        amount = int(value)
    except (TypeError, ValueError):
        return value
    return f"{amount:,}".replace(",", ".") + " ₫"
