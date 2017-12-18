import requests
import time
import agent
import random
import json
import re


class BussSpider:


    def __init__(self):
        self._time = str(time.time() * 1000)[:-4]
        self._gt = None
        self._challenge = None
        self.search_item_init()
        self.geetest_info = None

    def construct_header(self, **kwargs):
        header = {
            'User-Agent': random.choice(agent.agents),
        }
        if kwargs:
            header = dict(header, **kwargs)
        return header

    def get_response(self, url):
        response = requests.get(url, headers=self.construct_header())
        return response

    def get_content(self, url):
        response = self.get_response(url)
        if response.status_code == 200:
            return response.content
        else:
            print(url, response.status_code)
            raise response.status_code

    def search_item_init(self):
        content = self.get_content('http://www.gsxt.gov.cn/SearchItemCaptcha?v=' + self._time)
        res_dict = json.loads(content.decode())
        self._gt = res_dict.get('gt', '')
        self._challenge = res_dict.get('challenge', '')

    def get_geetest(self):
        """
        获取geetest信息
        :return:
        """
        pro = "http://"
        data_dict = {
            'gt': self._gt,
            'challenge': self._challenge,
            'product': 'popup',
            'offline': 'false',
            'protocol': pro,
            'type': 'slide',
            'path': '/static/js/geetest.6.0.1.js',
            'callback': 'geetest_' + self._time
        }
        url = "http://api.geetest.com/get.php"
        response = requests.get(url, params=data_dict, headers=self.construct_header())
        content = response.content.decode()
        res_str = re.findall(r'\((.*?)\)', content, re.DOTALL)
        if res_str:
            res_dict = json.loads(res_str[0])
            self.geetest_info = res_dict

    def get_bg_img(self):
        if self.geetest_info:
            url = 'http://'+self.geetest_info['static_servers']+self.geetest_info['fullbg']
            return  url


if __name__ == '__main__':
    spider = BussSpider()
    spider.construct_header(Referer='http://www.gsxt.gov.cn/index.html')
    spider.get_geetest()