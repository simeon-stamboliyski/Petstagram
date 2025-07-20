from django import template

register = template.Library()

@register.filter(is_safe=True)
def placeholder(field, text):
    field.field.widget.attrs['placeholder'] = text
    return field