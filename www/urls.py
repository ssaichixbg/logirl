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

urlpatterns = [
    url(r'^admin/', admin_site.urls),

    url(r'^about', dress.views.AboutView.as_view(), name=dress.views.AboutView.view_name),
    url(r'^item', dress.views.ItemDetail.as_view(), name=dress.views.ItemDetail.view_name),
    url(r'^donation', dress.views.DonationView.as_view(), name=dress.views.DonationView.view_name),
    url(r'^brand/', dress.views.BrandListView.as_view(), name=dress.views.BrandListView.view_name),
    url(r'^brand/type/(?P<brand_type>d+)', dress.views.BrandListView.as_view(), name=dress.views.BrandListView.view_name),

    url(r'^$', dress.views.HomeView.as_view(), name=dress.views.HomeView.view_name),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
