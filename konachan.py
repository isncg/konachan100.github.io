import json
import threading
import urllib
import urllib.request

import time

postlist = []

test_post_list = json.loads(open('testdata.json', 'r').read())



def webread(url, readtimeout=10):
    """read page"""
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'),
                         ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]
    return opener.open(url, None, readtimeout).read()

class DataSource:
    def URL(self):
        return None
    def Get(self):
        try:
            return json.loads(webread(self.URL()).decode())
        except Exception as e:
            return None

class DataSoruceS(DataSource):
    def URL(self):
        return "http://www.konachan.net/post.json?limit=100&rating:safe"

class DataSoruceQ(DataSource):
    def URL(self):
        return "http://www.konachan.net/post.json?limit=100&rating:questionable"

class DataSoruceE(DataSource):
    def URL(self):
        return "http://www.konachan.net/post.json?limit=100&rating:explicit"

class DataSourceTest(DataSource):
    def Get(self):
        return test_post_list


def update():
    global postlist
    try:
        newlist = json.loads(webread('http://www.konachan.net/post.json?limit=100').decode())
        for p in newlist:
            #print(p)
            p['file_url'] = p['file_url'].replace('konachan.net', 'konachan.com')
            p['jpeg_url'] = p['jpeg_url'].replace('konachan.net', 'konachan.com')
        postlist=newlist

    except Exception as e:
        print('Failed to get post list')


def update_loop():
    while True:
        update()
        time.sleep(300)

def start_update_thread():
    thread=threading.Thread(target=update_loop)
    thread.setDaemon(True)
    thread.start()
