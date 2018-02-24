from  __future__ import unicode_literals

import time
import random
import sys

import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class Weibo:
    URLS = {
        'home': 'http://weibo.com',
        'login': 'https://sae.sina.com.cn',
        'search_user': 'http://s.weibo.com/user/{kw}&Refer=weibo_user'
    }
    def __init__(self, username, password):
        opts = Options()
        # opts.add_argument("user-agent=" + get_random_user_agent())
        # opts.add_argument("--incognito")
        self.driver = webdriver.Chrome(chrome_options=opts)
        self.username = username
        self.password = password

    def login(self):
        jumped = False
        while not jumped:
            self.driver.get(Weibo.URLS['login'])
            userId = self.driver.find_element_by_id('userId')
            userId.send_keys(self.username)
            time.sleep(0.5)
            passwd = self.driver.find_element_by_id('passwd')
            passwd.send_keys(self.password)
            passwd.send_keys(Keys.RETURN)
            time.sleep(1.0)
            self.driver.find_element_by_class_name('WB_btn_login').click()
            time.sleep(0.8)
            self.driver.find_element_by_class_name('WB_btn_login').click()

            try:
                WebDriverWait(self.driver, 10).until(EC.url_contains('sinacloud.com/'))
                jumped = True
            except:
                jumped = False

        self.driver.get(Weibo.URLS['home'])


    def search_user(self, kw):
        current_url = self.driver.current_url
        jumped = False
        while not jumped:
            url = Weibo.URLS['search_user'].format(**locals())
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(EC.url_changes(current_url))
            jumped = '机器人' not in self.driver.page_source
            if not jumped:
                input('')

        soup = bs4.BeautifulSoup(self.driver.page_source, 'html.parser')
        for p in soup.select('.list_person'):
            url = 'https:' + p.select_one('.person_name').select_one('a')['href']
            brief = p.select_one('.person_info').get_text() if p.select_one('.person_info') else ''
            tags = p.select_one('.person_label').get_text() if p.select_one('.person_label') else ''
            if 'taobao' in brief or 'lolita' in brief.lower() or 'tb' in brief.lower() or '洋装' in brief or '店' in brief:
                return url
            if 'lolita' in tags or '洋装' in tags:
                return url

        return ''

if __name__ == '__main__':
    wb = Weibo(sys.argv[1], sys.argv[2])
    print('logging in')
    wb.login()
    print('logged in')
    data = open('data').readlines()[38+95+150:]
    i = 0
    for row in data:
        kw = row.split('https')[0].replace('\n','')
        if not kw:
            continue
        print(kw + '\t' + wb.search_user(kw) + '\t' + str(i))
        time.sleep(random.choice(range(2,10)))
        i+=1
