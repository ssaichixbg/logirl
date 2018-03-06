# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from www.admin import admin_site

from .models import *

# Register your models here.
@admin.register(Brand, site=admin_site)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'abbr', 'brand_type',)


@admin.register(Tag, site=admin_site)
class TagAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'english_name', 'external_id', 'attr_type', )


@admin.register(Feature, site=admin_site)
class FeaturedAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'english_name', 'external_id', 'attr_type',)


@admin.register(Color, site=admin_site)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'english_name', 'external_id', 'attr_type', )


# class ItemImageInline(admin.TabularInline):
#     model = ItemImage
#     extra = 1
#
#
# @admin.register(Item, site=admin_site)
# class ItemAdmin(admin.ModelAdmin):
#     list_display = ('display_name', 'type', 'year', 'month', 'url', 'price', 'price_currency', 'size')
#     inlines = (ItemImageInline, )
#
#
# @admin.register(CustomerImage, site=admin_site)
# class CustomerImageAdmin(admin.ModelAdmin):
#     list_display = ('dress', 'image', )
#
#
# @admin.register(ItemImage, site=admin_site)
# class ItemImageAdmin(admin.ModelAdmin):
#     list_display = ('dress', 'image', )
