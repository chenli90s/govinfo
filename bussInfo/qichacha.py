import requests
import agent
import random
from urllib import request
from lxml import etree
import pymongo
import html as Htmlparser
import re
import time


class QccSpider:
    def get_header(self, referer='http://www.qichacha.com'):
        header = {
            'user-agent': random.choice(agent.agents),
            'Referer': referer,
            'Cookie': 'UM_distinctid=16000b1545394-0817211ebed5ac-574e6e46-3d10d-16000b1545444; acw_tc=AQAAAHC1h1zlIgMAY1XOjM7EfwbsSt+w; _uab_collina=151184537293666344001779; PHPSESSID=a8k1l09d0ine3gbhvijg91gli6; hasShow=1; _umdata=BA335E4DD2FD504FF74B14E7F77EDA9BA74EDA3970E1B14984358C833F0952F0695B4A078346FD83CD43AD3E795C914C211C04857B0CA754C41141816A45307B; zg_did=%7B%22did%22%3A%20%2216000b15489102-04f718eab1e65b-574e6e46-3d10d-16000b1548ab1%22%7D; CNZZDATA1254842228=1809050604-1511840619-%7C1511853122; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201511857291095%2C%22updated%22%3A%201511858567704%2C%22info%22%3A%201511840109723%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%22a7621164b45dbce3271c1eaf4913afd7%22%7D',
        }
        return header

    def get_cookies(self):
        header = {
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
        }
        url = 'http://m.qichacha.com/'
        response = requests.get(url, headers=header)
        cookies = response.cookies
        cookies_dict = requests.utils.cookiejar_from_dict(cookies)
        return cookies_dict

    def get_response(self, url):
        response = requests.get(url, headers=self.get_header())
        if response.status_code == 200:
            return response
        else:
            print(url, '___', response.status_code)
            raise response.status_code

    def get_content(self, url):
        response = self.get_response(url)
        content = response.content
        return content.decode(response.encoding)

    def search(self, keywords):
        keywords = request.quote(keywords)
        # url = "https://m.qichacha.com/search?key=%s" % keywords
        url = 'http://www.qichacha.com/search?key=' + keywords
        res = self.get_content(url)
        html_content = etree.HTML(res)
        self.parse(html_content, url)
        for i in range(1, 11):
            time.sleep(5)
            self.link_follow(keywords, i)

    # 下一页
    def link_follow(self, keyword, index):
        url = "http://www.qichacha.com/search_index?key=%s&ajaxflag=1&p=%d&" % (keyword, index)
        res = self.get_content(url)
        html = etree.HTML(res)
        self.parse(html, url)

    def parse(self, content, url):
        item_list = content.xpath('//a[@class="ma_h1"]')
        if not item_list:
            print("%s地址数据不正确"%url)
            return None
        for item in item_list:
            res = self.get_detail(item)
            # print(res)
            html = etree.HTML(res)
            res_dict = self.parse_detail(html)
            res_dict = self.filter_info(res_dict)
            print(res_dict)
            self.save_db(res_dict)

    def get_detail(self, item):
        link = item.xpath('./@href')[0]
        res = etree.tostring(item)
        res = Htmlparser.unescape(res.decode())
        res = re.sub("<em>", "", res, res.count("<em>"), re.DOTALL)
        res = re.sub("</em>", "", res, res.count("</em>"), re.DOTALL)
        res = re.findall('>(.*?)<', res)[0]
        unique = link.split("_")[1].split('.')[0]
        companyname = res
        url = "http://www.qichacha.com/company_getinfos?unique=%s&companyname=%s&tab=base"%(unique, companyname)
        return self.get_content(url)

    @staticmethod
    def filter_info(res_dict):
        tem = {}
        for key, val in res_dict.items():
            # print(key, val)
            if isinstance(val, str):
                tem[key] = val.strip()
            elif isinstance(val, list) and val:
                tem[key] = val[0].strip()
        return tem


    def parse_detail(self, html):
        # 统一社会信用代码
        credit_code = html.xpath('//*[@id="Cominfo"]/table/tr[1]/td[2]/text()')
        # 纳税人识别号：
        taxpayer_code = html.xpath('//*[@id="Cominfo"]/table/tr[1]/td[4]/text()')
        # 注册号：
        regist_code = html.xpath('//*[@id="Cominfo"]/table/tr[2]/td[2]/text()')
        # 组织机构代码：
        org_code = html.xpath('//*[@id="Cominfo"]/table/tr[2]/td[4]/text()')
        # 法定代表人
        legal_man = html.xpath('//*[@id="Cominfo"]/table/tr[3]/td[2]/a[1]/text()')
        # 注册资本： registered capital
        registered_capital = html.xpath('//*[@id="Cominfo"]/table/tr[3]/td[4]/text()')
        # 经营状态：
        manage_status = html.xpath('//*[@id="Cominfo"]/table/tr[4]/td[2]/text()')
        # 成立日期：
        init_date = html.xpath('//*[@id="Cominfo"]/table/tr[3]/td[4]/text()')
        # 公司类型：
        company_type = html.xpath('//*[@id="Cominfo"]/table/tr[5]/td[2]/text()')
        # 营业期限
        manage_date = html.xpath('//*[@id="Cominfo"]/table/tr[6]/td[2]/text()')
        # 登记机关：
        sigind_depa = html.xpath('//*[@id="Cominfo"]/table/tr[5]/td[4]/text()')
        # 核准日期：)
        appr_date = html.xpath('//*[@id="Cominfo"]/table/tr[7]/td[2]/text()')
        return locals()

    def save_db(self, res_dict):
        client = pymongo.MongoClient('127.0.0.1', 27017)
        db = client['dept_info']
        collection = db['detail_info']
        collection.insert(res_dict)

if __name__ == '__main__':
    spider = QccSpider()
    spider.search("腾讯")
