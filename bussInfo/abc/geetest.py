import requests
from lxml import etree
import sys


def get_content():
    response = requests.get('http://hanyu.iciba.com/zt/3500.html')
    # text = response.text
    ht = etree.HTML(response.content.decode())
    eles = ht.xpath('//a/text()')
    keys = []
    for ele in eles:
        if len(ele) < 2:
            keys.append(ele)
    print(len(keys))
    sys.setrecursionlimit(1000000)
    akak = get_keys(keys)
    print(akak)


def get_keys(keys):
    f = open('keys.py', 'wb')
    akak = []
    for _ in keys:
        for key in keys:
            # akak.append(keys[_]+key)
            print(_+key)
            key = _+key+'\n'
            f.write(key.encode())
    f.close()
    return akak


if __name__ == '__main__':
    get_content()
