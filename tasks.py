import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "www.settings")
django.setup()

from collector.lolibrary.tasks import *

def sync_lolibrary():
    api = Lolibrary()

    sync_tags(api)
    sync_features(api)
    sync_colors(api)
    sync_brands(api)


if __name__ == '__main__':
    sync_lolibrary()