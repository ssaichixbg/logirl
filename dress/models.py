# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField

class DressBaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # Set this model as Abstract

    def __str__(self):
        return self.__getattribute__('display_name')


BrandFlags = (

)

BrandTypes = (
    (0, u'国牌'),
    (1, u'日牌'),
)


# Create your models here.
class Brand(DressBaseModel):
    display_name = models.CharField(max_length=200, verbose_name='名称')
    url = models.URLField(blank=True, null=True, verbose_name='网站')
    flag = models.IntegerField(choices=BrandFlags, default=0)
    brand_type = models.IntegerField(choices=BrandTypes, verbose_name='类别')
    image = models.ImageField(blank=True, null=True, upload_to='brand_images', verbose_name='Logo')
    isCopycat = models.BooleanField(default=False, verbose_name='山寨')
    abbr = models.CharField(max_length=200, null=True, blank=True, verbose_name='简称')
    weibo = models.URLField(null=True, blank=True, verbose_name='微博')
    twitter = models.URLField(null=True, blank=True, verbose_name='Twitter')

    class Meta:
        verbose_name = '品牌'
        verbose_name_plural = '品牌'

    @property
    def item_count(self):
        return self.item_set.count()

    @staticmethod
    def get_searchbar_all():
        return Brand.objects.all().order_by('display_name')

    @staticmethod
    def get_home_all(brand_type):
        return sorted(list(Brand.objects.all().filter(brand_type=brand_type)), key=lambda b: b.item_count)


AttributeType = (
    (0, 'lolib basic'),
    (1, 'lolib extended'),

)
class Tag(DressBaseModel):
    display_name = models.CharField(max_length=100)
    english_name = models.CharField(max_length=100, blank=True, null=True)
    external_id = models.CharField(max_length=100, blank=True, null=True)
    attr_type = models.IntegerField(choices=AttributeType, default=0)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'

    @staticmethod
    def get_searchbar_all():
        return Color.objects.all().filter(attr_type=0).order_by('display_name')


class Feature(DressBaseModel):
    display_name = models.CharField(max_length=100)
    english_name = models.CharField(max_length=100, blank=True, null=True)
    external_id = models.CharField(max_length=100, blank=True, null=True)
    attr_type = models.IntegerField(choices=AttributeType, default=0)

    class Meta:
        verbose_name = '特点'
        verbose_name_plural = '特点'

    @staticmethod
    def get_searchbar_all():
        return Feature.objects.all().filter(attr_type=0).order_by('display_name')


class Color(DressBaseModel):
    display_name = models.CharField(max_length=100)
    english_name = models.CharField(max_length=100, blank=True, null=True)
    external_id = models.CharField(max_length=100, blank=True, null=True)
    attr_type = models.IntegerField(choices=AttributeType, default=0)

    rgb = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        verbose_name = '颜色'
        verbose_name_plural = '颜色'

    @staticmethod
    def get_searchbar_all():
        return Color.objects.all().filter(attr_type=0).order_by('display_name')


ItemType = (
    (0, u'JSK'),
    (1, u'OP'),
    (2, u'SK'),
)

ItemStatus = (
    (0, u'在贩'),
    (1, u'征集'),
    (2, u'定金'),
    (3, u'补款'),
    (4, u'终止'),
)

Currency = (
    (0, u'人民币'),
    (1, u'日元'),
    (2, u'美元'),
)

ItemSize = (
    (0, u'XS'),
    (1, u'S'),
    (2, u'M'),
    (3, u'L'),
    (4, u'XL')
)


# class Item(DressBaseModel):
#     display_name = models.CharField(max_length=200, verbose_name='名称')
#     subtitle = models.CharField(max_length=200, default='', verbose_name='其它名称')
#     brand = models.ForeignKey(Brand)
#     type = models.IntegerField(choices=ItemType, verbose_name='商品类别')
#     year = models.IntegerField(null=True, blank=True, verbose_name='发售年')
#     month = models.IntegerField(null=True, blank=True, verbose_name='发售月')
#     prodNumber = models.CharField(max_length=200, null=True, blank=True, verbose_name='商品号')
#     url = models.URLField(blank=True, null=True, verbose_name='链接')
#     notes = models.CharField(max_length=400, null=True, blank=True, verbose_name='备注')
#     price = models.FloatField(null=True, blank=True, verbose_name='价格')
#     price_currency = models.IntegerField(choices=Currency, null=True, blank=True, verbose_name='价格货币')
#     submitter = models.CharField(max_length=200, null=True, blank=True, verbose_name='上传者')
#     copyItem = models.ForeignKey("self", null=True, blank=True, verbose_name='原版商品')
#     status = models.IntegerField(choices=ItemStatus, default=4)
#     presale_stop = models.DateField(blank=True, null=True)
#
#     # size
#     size = ArrayField(models.IntegerField(choices=ItemSize), blank=True)
#     size_json = JSONField(blank=True, default={})
#     # xs_bust_from = models.IntegerField(null=True, blank=True)
#     # xs_bust_to = models.IntegerField(null=True, blank=True)
#     # xs_length = models.IntegerField(null=True, blank=True)
#     # xs_waist_from = models.IntegerField(null=True, blank=True)
#     # xs_waist_to = models.IntegerField(null=True, blank=True)
#     # xs_shoulder = models.IntegerField(null=True, blank=True)
#     # xs_sleeve = models.IntegerField(null=True, blank=True)
#
#     dress_color = models.ManyToManyField(Color, blank=True, verbose_name='颜色')
#     dress_tag = models.ManyToManyField(Tag, blank=True)
#     dress_feature = models.ManyToManyField(Feature, blank=True, verbose_name='特点')
#
#     material = models.CharField(max_length=200, default='', blank=True, verbose_name='材质')
#
#     class Meta:
#         verbose_name = '商品'
#         verbose_name_plural = '商品'
#
#
# class ItemImage(DressBaseModel):
#     dress = models.ForeignKey(Item, verbose_name='商品')
#     image = models.ImageField(upload_to='item_images', verbose_name='图片')
#
#     def __str__(self):
#         return str(self.dress)
#
#     class Meta:
#         verbose_name = '商品照片'
#         verbose_name_plural = '商品照片'
#
#
# class CustomerImage(DressBaseModel):
#     dress = models.ForeignKey(Item, verbose_name='商品')
#     image = models.ImageField(upload_to='customer_images', verbose_name='图片')
#
#     def __str__(self):
#         return str(self.dress)
#
#     class Meta:
#         verbose_name = '返图'
#         verbose_name_plural = '返图'