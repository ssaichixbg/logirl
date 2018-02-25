from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from .views import *

url_bind = lambda *args: url(args[0], args[1].as_view(), name=args[1].view_name)

urlpatterns = [
    url(r'^shell/item', receive_shell_item),
]