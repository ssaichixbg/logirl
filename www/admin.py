# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.admin import AdminSite

class LoGirlAdminSite(AdminSite):
    site_title = 'Lo娘百科'
    site_header = 'Lo娘百科'
    index_title = '后台管理'

admin_site = LoGirlAdminSite()