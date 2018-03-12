import sys
import json
import urllib.request
import urllib.parse
import requests
import io
import traceback

import oss2

from shellolita.api import Shellolita


def fetch(host, start=0):
    sl = Shellolita(352)
    while not sl.EOF:
        sl.go_to_next_page()
        for url in sl.item_list[1:]:
            item = sl.get_item_detail(url)
            if not item:
                continue
            re = urllib.request.urlopen(host + '/_collector/shell/item', data=json.dumps(item).encode('utf-8')).read()
            if not re == b'0':
                print(url)
                return


def fetch_imgs(host, key_id, key_sec):
    item = json.loads(urllib.request.urlopen(host+'/_collector/shell/item').read())
    auth = oss2.Auth(key_id, key_sec)
    bucket = oss2.Bucket(auth, 'http://oss-cn-hangzhou.aliyuncs.com', 'logirl-shell')
    while item:
        ref_url = item['ref_url']
        print(ref_url)
        for img_url in item['imgs']:
            f = io.BytesIO()
            img = requests.get(
                'http://www-shellolita-com-static.smartgslb.com' + img_url,
                headers={
                    'Referer': ref_url,
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'
                })
            print(img_url)
            if not img.ok and not img.status_code == 404:
                input('error')
            f.write(img.content)
            f.seek(0)
            bucket.put_object(img_url[1:], f)
        req = urllib.request.urlopen(host+'/_collector/shell/item', data=json.dumps({
            'ref_url': ref_url,
            'url': ref_url,
            'stage': 1
        }).encode('utf-8'))
        if not req.read() == b'0':
            print('error')
            return

        item = json.loads(urllib.request.urlopen(host + '/_collector/shell/item').read())

    return True

if __name__ == '__main__':
    #fetch(sys.argv[1])
    suc = False
    while not suc:
        try:
            suc = fetch_imgs(sys.argv[1], sys.argv[2], sys.argv[3])
        except Exception as e:
            traceback.print_exc()
    print('Finished!')