'''
customfilters.py
--------------
Custom filters for use with HTML templates.
'''

from django import template

register = template.Library()

@register.filter
def get_field(fields, key):
    return fields[key].label_tag