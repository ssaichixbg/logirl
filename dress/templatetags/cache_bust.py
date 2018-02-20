import uuid

from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
register = template.Library()


@register.simple_tag
def static(value):
    value = settings.STATIC_URL + value

    if settings.DEBUG:
        version = uuid.uuid1()
    else:
        version = settings.get('PROJECT_VERSION')
        if version is None:
            version = '1'

    if '?' in value:
        return value + '&__v__={version}'.format(version=version)
    else:
        return value + '?__v__={version}'.format(version=version)