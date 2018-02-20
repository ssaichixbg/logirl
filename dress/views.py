# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import inspect

from django.http import Http404
from django.views.generic import TemplateView
from django.views.generic.list import MultipleObjectMixin
from django.core.urlresolvers import reverse

from utils.decorator import *
import utils.html_tag as tag

import dress.models as models


class BaseView(TemplateView):

    nav_title = ''
    view_name = ''

    @property
    def nav_views(self):
        return [HomeView, BrandListView, AboutView, DonationView, ]

    @property
    def meta(self):
        return {
            'title': self.__class__.nav_title
        }

    def __get_all_properties(self):
        return {i[0]: i[1] for i in inspect.getmembers(self)
                if not i[0].startswith('_') and not inspect.ismethod(i[1]) and not inspect.isclass(i[1])}

    def get_context_data(self, **kwargs):
        ctx = super(BaseView, self).get_context_data(**kwargs)
        ctx.update(self.__get_all_properties())
        return ctx


class SearchResultView(BaseView):

    view_name = 'search_result'

    template_name = 'search_result.html'

    class Item():
        def __init__(self):
            self.display_name = tag.a()
            self.subtitle = ''
            self.image_url = ''
            self.contributor_name = ''
            self.type = tag.a()
            self.date = ''
            self.brand = tag.a()

        @staticmethod
        def mock(i):
            item = SearchResultView.Item()
            item.display_name = tag.a('标题 ' + str(i), href=reverse(ItemDetail.view_name))
            item.subtitle = '副标题 12345' + str(i)
            item.image_url = 'https://images.lolibrary.org/file/lolibrary-images/4e97eb15-6d11-4f45-bd12-272d53e3fc4a_thumb.jpeg'
            item.contributor_name = 'XXX'
            item.type = tag.a('JSK')
            item.date = '2017.10'
            item.brand = tag.a('MILK')
            return item

    @property
    def order_display_names(self):
        return (
            ('-time', '最新'),
            ('price', '价格高->低',),
            ('-price', '价格低->高'),
            ('-hot', '人气'),
        )

    @property
    @GET
    def items(self, kw='', order='-time', brand=None, feature=None, tag=None, type=None, color=None, page=0):
        r = [SearchResultView.Item.mock(i) for i in range(int(page) * 10, 10 + int(page) * 10)]
        return r if int(page) <= 2 else []

    @property
    @GET
    def form_data(self, **kwargs):
        advance_set = ['brand', 'feature', 'tag', 'type', 'color']
        if (any([kwargs.get(k) for k in advance_set])):
            kwargs['show_advance_search'] = True

        kwargs.setdefault('order', '-time')
        kwargs['order_display_name'] = dict(self.order_display_names).get(kwargs['order'])
        return kwargs


class HomeView(SearchResultView):

    nav_title = '主页'
    view_name = 'home'

    template_name = 'search.html'

    @property
    def searchbar(self):
        return {
            'item_types': models.ItemType,
            'colors': models.Color.get_searchbar_all(),
            'features': models.Feature.get_searchbar_all(),
            'brands': models.Brand.get_searchbar_all()
        }


class BrandListView(BaseView):

    nav_title = 'Lo牌列表'
    view_name = 'brand_list'

    template_name = 'brands_list.html'

    @property
    def brands(self):
        types = [i[0] for i in models.BrandTypes]
        brand_type = self.kwargs.get('brand_type', 0)
        if not brand_type in types:
            raise Http404

        return models.Brand.get_home_all(brand_type)


class ItemDetail(BaseView):

    view_name = 'item_detail'

    template_name = 'item_detail.html'

    @property
    def images(self):
        images = [
            'https://images.lolibrary.org/file/lolibrary-images/a52282ad-55a9-4b4e-8c01-e0dbb1f3be91.jpeg',
            'https://images.lolibrary.org/file/lolibrary-images/49035f39-130b-480c-8e2f-3c8c765f2dc9.jpeg',
            'https://images.lolibrary.org/file/lolibrary-images/d4f3dcc0-db28-4d7a-9ebc-f0d27dcea2cb.jpeg',
            'https://images.lolibrary.org/file/lolibrary-images/e1ad6ca0-9466-4220-9f5b-e218c0da5ae6.png',

        ]
        return images

    @property
    def details(self):
        def _create_entry(key, a=None, text=None):
            return {'key': key, 'a': a, 'text': text}

        details = [
            _create_entry('牌子', a=[tag.a('MILK')]),
            _create_entry('类型', a=[tag.a('JSK')]),
            _create_entry('发售时间', text='2017 7月'),
            _create_entry('颜色', a=[tag.a('红色'), tag.a('白色')]),
            _create_entry('版型', a=[tag.a('小高腰'), tag.a('娃娃袖')]),
            _create_entry('价格', text='21000 日元'),
            _create_entry('备注', text='1\n2\n3'),
            _create_entry('修订小天使', a=[tag.a('AAA')]),
            _create_entry('标签', a=[tag.a('BBB')]),
        ]
        return details


class AboutView(BaseView):

    nav_title = '加入我们'
    view_name = 'about'

    template_name = 'join_us.html'


class DonationView(BaseView):

    nav_title = '投喂'
    view_name = 'donation'

    template_name = 'donation.html'