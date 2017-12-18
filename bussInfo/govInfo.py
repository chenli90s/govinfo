import requests
import time
import json
import random
import datetime
import re
from urllib import request

header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Host': 'www.gsxt.gov.cn',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'Referer': 'http://www.gsxt.gov.cn/index',
}


class GsxtInfo:

    def __init__(self):
        self.start_url = 'http://www.gsxt.gov.cn/SearchItemCaptcha?v=' + str(
            int(time.time())) + "000"
        self.search_url = 'http://www.gsxt.gov.cn/corp-query-search-1.html'
        self.user = 'mrcro90s'
        self.passwd = '644973346'
        self.session = requests.session()
        # self.session.get('http://www.gsxt.gov.cn/index.html')

    def get_response(self, url):
        response = self.session.get(url, headers=header)
        return response

    def log(self, res):
        print('***********************')
        print('**                   **')
        print('**    请不成功%d   **' % res.status_code)
        print('**                   **')
        print('***********************')

    def get_content(self, url):
        res = self.get_response(url)
        if res.status_code == 200:
            return res.content
        else:
            self.log(res)
            print(url)

    def post_content(self, url, data):
        headers = {
            'Host':'www.gsxt.gov.cn',
            'Origin':'http://www.gsxt.gov.cn',
            'Proxy-Connection':'keep-alive',
            'Referer':'http://www.gsxt.gov.cn/corp-query-homepage.html',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Cache-Control':'max-age=0',
            'Content-Length':'218',
            'Content-Type':'application/x-www-form-urlencoded',
        }
        response = self.session.post(url, data=data, headers=headers)
        if response.status_code == 200:
            return response.content
        else:
            self.log(response)

    def get_gt(self):
        res = self.get_content(self.start_url)
        if res:
            res_dict = json.loads(res.decode())
            self.gt = res_dict['gt']
            self.challenge = res_dict['challenge']
            return True

    def gt_jiyan(self):
        con_url = 'http://jiyanapi.c2567.com/shibie?gt=%s&challenge=%s&referer=%s&user=%s&pass=%s&return=json' % (
            self.gt, self.challenge, header['Referer'], self.user, self.passwd)
        print(con_url)
        res = self.get_response(con_url)
        if res:
            print(res.text)
            res_dict = json.loads(res.text)
            if res_dict['status'] == 'ok':
                self.validate = res_dict['validate']
                return True

    def decode_arry(self, url):
        res = self.get_content(url).decode()
        res = res[1:-1].split(',')
        strs = ''
        for str in res:
            strs += chr(int(str))
        print(strs)
        return strs

    def fwtj_vaildate(self):
        cookies_dict = requests.utils.dict_from_cookiejar(self.session.cookies)
        jsession_id = cookies_dict['JSESSIONID'].split(':')[0]
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'fwtj.gsxt.gov.cn',
            'Origin': 'http://www.gsxt.gov.cn',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://www.gsxt.gov.cn/index.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        }
        data = {
            'param': "{'sessionId':'"+jsession_id+"','referer':'','host':'www.gsxt.gov.cn','url':'http://www.gsxt.gov.cn/index.html','queryString':'','nodenum':'999999'}"
        }
        url = 'http://fwtj.gsxt.gov.cn/statistics/collectT1Log'
        print(url)
        res = requests.get(url, data=data, headers=headers).content
        print(res)

    def get_token(self):
        first_url = 'http://www.gsxt.gov.cn/corp-query-custom-geetest-image.gif?v='
        time = datetime.datetime.now()
        v = time.minute + time.second
        start_url = first_url + str(v)
        strs = self.decode_arry(start_url)
        one_codes = re.findall(r'(\d+)', strs, re.DOTALL)
        print(one_codes)
        data_code = one_codes[0]
        one_code = one_codes[1]
        # self.fwtj_vaildate()
        sec_url = 'http://www.gsxt.gov.cn/corp-query-geetest-validate-input.html?token=' + one_code
        print(sec_url)
        strs = self.decode_arry(sec_url)
        sec_code = re.findall(r'value: (\d+)}', strs)
        print(sec_code)
        self.token = int(sec_code[0]) ^ int(data_code)
        print(self.token)

    def search(self, key=''):
        result = self.get_content(
            'http://www.gsxt.gov.cn/corp-query-search-test.html?searchword=' + request.quote(key))
        print(result)
        form_data = {
            'tab': 'ent_tab',
            'token': self.token,
            'searchword': key,
            'geetest_challenge': self.challenge,
            'geetest_validate': self.validate,
            'geetest_seccode': self.validate + '|jordan',
        }

        print(form_data)
        time.sleep(10)
        res = self.post_content(self.search_url, form_data)
        if res:
            res = res.decode()
            print(res)

    def main(self):
        self.get_content('http://www.gsxt.gov.cn/index.html')
        res = self.get_gt()
        self.get_token()
        res = res and self.gt_jiyan()
        count = 0
        while not res and count < 3:
            count += 1
            res = self.get_gt()
            res = res and self.gt_jiyan()
        self.search('百度')


if __name__ == '__main__':
    info = GsxtInfo()
    info.main()
    # info.search()
