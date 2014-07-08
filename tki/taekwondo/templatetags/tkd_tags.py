from django.core.urlresolvers import resolve
from django import template

register = template.Library()

@register.simple_tag
def active(request, url):
    
    url_name = resolve(request.path).url_name
    if url_name == url:
        return "active"
    return ""    