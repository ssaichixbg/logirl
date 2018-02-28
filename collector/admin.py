# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from www.admin import admin_site

from .models import *

# Register your models here.
@admin.register(ShellData, site=admin_site)
class ShellDataAdmin(admin.ModelAdmin):
    list_display = ('title', 'ref_url', 'stage', )