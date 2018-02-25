# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *
# Create your views here.

@csrf_exempt
def receive_shell_item(request):
    data = json.loads(request.body.decode('utf-8'))

    shell_item, created = ShellData.objects.all().get_or_create(ref_url=data['url'])

    shell_item.title = data['title']
    shell_item.brand = data['brand']
    shell_item.content = data['content']
    shell_item.tags = data['tags']
    shell_item.ref_url = data['url']
    shell_item.save()

    return HttpResponse('0')