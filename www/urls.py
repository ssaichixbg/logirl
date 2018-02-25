"""logirl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from .admin import admin_site

import dress.views

url_bind = lambda *args: url(args[0], args[1].as_view(), name=args[1].view_name)

urlpatterns = [
    url(r'^admin/', admin_site.urls),

    url_bind(r'^about$', dress.views.AboutView),
    url_bind(r'^donation$', dress.views.DonationView),
    url_bind(r'^contributor$', dress.views.ContributorView),

    url_bind(r'^item', dress.views.ItemDetail),
    url_bind(r'^brand/', dress.views.BrandListView),
    url_bind(r'^brand/type/(?P<brand_type>d+)', dress.views.BrandListView),
    url_bind(r'^search$', dress.views.SearchResultView),
    url_bind(r'^$', dress.views.HomeView),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    url(r'^_collector/', include('collector.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
