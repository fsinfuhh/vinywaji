from django import template

register = template.Library()


@register.filter
def toEuro(value):
    try:
        value = int(value) / 100
        return f"{value:.2f}"
    except:
        pass
    return ""
