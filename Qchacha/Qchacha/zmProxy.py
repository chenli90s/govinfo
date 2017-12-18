import requests
import json
class ZmProxy:


    def  __init__(self):
        self._url = 'http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=0&city=0&yys=0&port=1&time=1&ts=1&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions='
        self.get_balance_url = 'http://web.http.cnapi.cc/index/index/get_my_balance?neek=32044&appkey=f52ae2f99252050df5e76b8e045d07c0'
        self.set_ip_line_url = 'web.http.cnapi.cc/index/index/save_white?neek=32044&appkey=f52ae2f99252050df5e76b8e045d07c0&white='

    def get_content(self, url):
        response = requests.get(url)
        content = response.content.decode()
        return json.loads(content)

    """
    {"code":0,"success":success,"msg":"0","data":[{"ip":"27.209.166.95","port":52136,"expire_time":"2017-12-05 09:51:50"},{"ip":"60.189.144.251","port":55764,"expire_time":"2017-12-05 09:57:13"},{"ip":"119.115.27.110","port":8943,"expire_time":"2017-12-05 09:58:28"},{"ip":"182.107.77.239","port":59756,"expire_time":"2017-12-05 10:01:03"},{"ip":"123.156.24.170","port":52156,"expire_time":"2017-12-05 09:49:02"}]}
    """

    def get_proxy_ip(self):
        res = self.get_content(self._url)
        print('成功获取')
        if res['success']:
           return res['data']

    def get_balance(self):
        res = self.get_content(self.get_balance_url)
        if res['success']:
           return res['data']['balance']


    def set_ip_line(self, ip):
        url = self.set_ip_line_url + ip
        res = self.get_content(url)
        if res['success']:
           return True
