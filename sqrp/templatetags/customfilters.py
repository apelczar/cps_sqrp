'''
customfilters.py
--------------
Custom filters for use with HTML templates.
'''

from django import template

register = template.Library()

@register.filter
def base64_decode(value):
    return value.decode('utf-8')