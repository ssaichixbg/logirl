# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import urllib.parse

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import bs4

from .models import *
# Create your views here.


def get_shell_item(request):
    unpic = ShellData.objects.all().filter(stage=0)
    if unpic:
        data = unpic[0].content
        soup = bs4.BeautifulSoup(data, 'html.parser')
        imgs = [img.attrs['src'] for img in soup.select('img')]
        imgs = ['-'.join(img.split('.')[0].split('-')[:-1]) + '.' + img.split('.')[1] for img in imgs if 'upload' in img]
        return JsonResponse({
            'imgs': imgs,
            'ref_url': unpic[0].ref_url
        })
    else:
        return JsonResponse({})

@csrf_exempt
def receive_shell_item(request):
    if request.method == 'GET':
        return get_shell_item(request)

    data = json.loads(request.body.decode('utf-8'))

    shell_item, created = ShellData.objects.all().get_or_create(ref_url=data['url'])

    if data.get('ref_url'):
        shell_item.stage = data['stage']
        shell_item.save()
        return HttpResponse('0')

    shell_item.title = data['title']
    shell_item.brand = data['brand']
    shell_item.content = data['content']
    shell_item.tags = data['tags']
    shell_item.ref_url = data['url']
    shell_item.save()

    return HttpResponse('0')