from django import template

register = template.Library()

@register.filter
def get_field(fields, key):
    return fields[key].label_tag