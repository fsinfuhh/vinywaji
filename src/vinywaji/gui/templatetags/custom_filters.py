from django import template

register = template.Library()


@register.filter
def toeuro(value):
    try:
        value = int(value) / 100
        return f"{value:.2f}"
    except:
        pass
    return ""
