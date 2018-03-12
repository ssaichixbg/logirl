import requests
import io
import logging

from django.core.files.uploadedfile import SimpleUploadedFile

from dress.models import *

from .api import Lolibrary

logger = logging.getLogger(__name__)


def __sync_model(api, model, entity):
    logger.info('start syncing {0} with {1}...'.format(model.__name__, entity))
    items = api.get_list(entity, auto_page=True)

    for item in items:
        logger.info('color slug: {slug}'.format(**item))
        # synced before
        record = model.objects.all().filter(external_id=item['slug'], external_src=1)
        if record:
            logger.info('found in external id')
            record = record[0]
            record.english_name = item['name']
            record.save()
            continue

        # not synced but has translation
        record = model.objects.all().filter(english_name=item['name'], external_src__isnull=True)
        if record:
            logger.info('found in english name')
            record = record[0]
            record.external_id = item['slug']
            record.external_src = 1
            record.save()
            continue

        logger.info('create new one')
            # new one
        _ = model.objects.create(
            display_name=item['name'],
            english_name=item['name'],
            external_id=item['slug'],
            attr_type=3
        )

    logger.info('finished syncing')


def sync_colors(api):
    """
    Sync color
    :param api: Lolibrary
    :return:
    """
    __sync_model(api, Color, Lolibrary.RESTfulEntity.Colors)


def sync_tags(api):
    """

    :param api: Lolibrary
    :return:
    """
    __sync_model(api, Tag, Lolibrary.RESTfulEntity.Tags)


def sync_features(api):
    '''

    :param api: Lolibrary
    :return:
    '''
    __sync_model(api, Feature, Lolibrary.RESTfulEntity.Features)

def sync_brands(api):
    """
    Sync brands
    :param api: Lolibrary
    :return:
    """
    def get_img(url):
        new_img = io.BytesIO()
        logger.info('downloading image: {0}'.format(url))
        img = requests.get(
            url,
            headers={
                'Referer': '',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'
            })
        if not img.ok:
            logger.error('result code is not OK')
            new_img.close()
            return None, 0

        length = new_img.write(img.content)
        new_img.seek(0)
        return new_img, length

    logger.info('start syncing brands...')
    items =  api.get_list(api.RESTfulEntity.Brands)
    lolib_map = {
        'slug': 'external_id',
        'name': 'display_name',
        'short_name': 'abbr',
    }

    for item in items:
        logger.info('brand slug: {slug}'.format(**item))

        brand, created = Brand.objects.get_or_create(external_id=item['slug'], external_src=1, brand_type=1)
        if created:
            logger.info('new record')
        for k, v in lolib_map.items():
            brand.__setattr__(v, item[k])

        ori_img_size = brand.image.size if brand.image else 0
        new_img, new_img_len = get_img(item['image']['url'])
        if ori_img_size == new_img_len:
            if ori_img_size:
                logger.info('image not changed')
            else:
                logger.info('image is null')
        else:
            logger.info('updating image...')
            django_file = SimpleUploadedFile(item['image']['url'].split('/')[-1], new_img.read())
            brand.image = django_file

        brand.save()

    logger.info('finished brands syncing')


def sync_categories(api):
    '''

    :param api: Lolibrary
    :return:
    '''
