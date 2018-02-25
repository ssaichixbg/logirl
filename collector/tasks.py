import sys

import json
import urllib.request

from shellolita.api import Shellolita


def fetch(host, start=0):
    sl = Shellolita()
    while not sl.EOF:
        sl.go_to_next_page()
        for url in sl.item_list[1:]:
            item = sl.get_item_detail(url)
            if not item:
                continue
            re = urllib.request.urlopen(host + '/_collector/shell/item', data=json.dumps(item).encode('utf-8')).read()
            if not re == b'0':
                print(url)


if __name__ == '__main__':
    fetch(sys.argv[1])