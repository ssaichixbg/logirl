from urllib.request import urlopen, Request
from urllib.parse import urlencode
import json
import logging

from django.conf import settings
import bs4

logger = logging.getLogger(__name__)


def sp(data):
    return bs4.BeautifulSoup(data, 'html.parser')


class Lolibrary:
    class RESTfulEntity:
        Brands = '/brands'
        Categories = '/categories'
        Features = '/features'
        Colors = '/colors'
        Tags = '/tags'
        Items = '/items'

    class URL:
        search = '/search'

    BaseURL = settings.LOLIBRARY_BASE_URL

    def __init__(self):
        pass

    def get_page(self, url):
        req = Request(
            self.BaseURL + url,
            headers={
                'User-Agent': 'python/cn/lolibrary'
            },
        )
        logger.info('get url: {0}'.format(url))
        return urlopen(req).read()

    def get_json(self, url):
        return json.loads(self.get_page(url).decode('UTF-8'))

    def get_list(self, entity, kw=None, page=None, auto_page=False):
        if kw:
            result = self.get_json('{}/search?{}'
                                   .format(entity, urlencode({'search': kw})))
        else:
            result = self.get_json(entity)
            if isinstance(result, dict) and not page and auto_page:
                last_page = result['last_page']
                result_list = result['data']
                result_list.extend([data
                                    for page in range(1, last_page + 1)
                                    for data in self.get_json('{}?page={}'.format(entity, page))['data']])
                result = result_list
        return result

    def get_detail(self, entity, slug):
        result = self.get_json('{0}/{1}'.format(entity, slug))
        return result


if __name__ == '__main__':
    pass