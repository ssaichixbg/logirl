from urllib.request import urlopen, Request

import bs4

def get_page(url):
    print('visiting %s...' % url)
    req = Request(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        },
    )
    return urlopen(req).read()

def sp(data):
    return bs4.BeautifulSoup(data, 'html.parser')


class Shellolita:
    URLs = {
        'page': 'http://www.shellolita.com/?paged=%d'
    }
    def __init__(self, page = 0):
        self.current_page = page
        self.EOF = False

        self.item_list = []

    def go_to_next_page(self):
        result = get_page(Shellolita.URLs['page'] % (self.current_page+1))
        soup = sp(result)
        self.item_list = []
        for entry in soup.select('.entry-title'):
            url = entry.select_one('a').attrs['href']
            self.item_list.append(url)

        self.EOF = not soup.select_one('.nav-previous')

        self.current_page += 1

    def get_item_detail(self, url):
        result = get_page(url)
        soup = sp(result)
        if not soup.select_one('.tag-links'):
            return

        title = soup.select_one('.entry-title').get_text()
        cats = [a.get_text() for a in soup.select_one('.cat-links').select('a')]
        tags = [a.get_text() for a in soup.select_one('.tag-links').select('a')]
        content = soup.select_one('.entry-content')

        brands = [b for b in cats if not b == 'Chinese Lolita']
        brand = brands[0] if len(brands) > 0 else ''
        imgs = []
        for img in content.select('img'):
            src = img.attrs['src']
            imgs.append(src)
            if 'com' not in src:
                img.decompose()
                continue
            img.attrs['src'] = src.split('.com')[1]

        return {
            'title': title,
            'brand': brand,
            'content': str(content),
            'tags': tags,
            'url': url
        }
