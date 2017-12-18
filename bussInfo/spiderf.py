import requests
import re
import os
import queue


class MainSpider(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
        'Referer': 'http://www.gsxt.gov.cn/index.html'
    }

    def __init__(self, path="ptml"):
        self.path = path
        self.css_path = path + "/css/"
        self.js_path = path + "/js/"
        self.img_path = path + "/img/"
        self.u_set = set()
        self.js_key_words = None
        self.css_key_words = None

    def main(self, url, path="ptml"):
        response = self.get_response(url)
        # init_page = response.content
        # self.f_loader(init_page, path + "/index.html")
        domains = re.findall(r"http://[\w\.]*", url)
        if not domains:
            domains = re.findall(r"https://[\w\.]*", url)
        domain = domains[0]
        self.process(response, domain)

    def main_from_post(self, url, form_data=None, path="ptml"):
        response = self.post_response(url, form_data)
        # init_page = response.content
        # self.f_loader(init_page, path + "/index.html")
        domains = re.findall(r"http://[\w\.]*", url)
        if not domains:
            domains = re.findall(r"https://[\w\.]*", url)
        domain = domains[0]
        self.process(response, domain)

    def process(self, response, domain):
        self.parse_content(response, domain)
        # try:
        #     self.parse_content(response, domain)
        # except Exception as e:
        #     print(e)

    def get_response(self, url):
        print(url)
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response
        else:
            print(response.url, response.status_code)
            raise response.status_code

    def get_content(self, url):
        return self.get_response(url).content

    def post_response(self, url, from_data=None):
        print(url)
        response = requests.post(url, headers=self.headers, data=from_data)
        if response.status_code == 200:
            return response
        else:
            print(response.url, response.status_code)
            raise response.status_code

    def post_content(self, url, data_form=None):
        return self.post_response(url, data_form).content


    def get_content_perfix(self, url, domain):
        res = url.split(":")
        if len(res) == 1:
            rss = re.match(r"^//", url)
            if rss:
                if domain:
                    hs = domain.split(':')[0]
                    url = hs + ":" + url
                else:
                    raise 'Domain is None'
            elif url[:3] == "../":
                url = domain + url[2:]
            else:
                if url[:3] == "./":
                    url = domain + url[1:]
                else:
                    url = domain + url
        return url

    # 处理静态文件
    def parse_content(self, response, domain=None):
        content = response.content.decode(response.encoding)
        content = self.parse_css(content, domain)
        content = self.parse_script(content, domain)
        content = self.parse_img(content, domain)
        self.f_loader(content.encode(), self.path + "/index.html")

    # 解析链接类型
    def parse_core(self, content, r, type, domain, file_path=""):
        # res = re.findall(r'<link.*?href="(.*?)".*?/>', content, re.DOTALL)
        res = r
        for ress in res:
            # print(ress)
            rss = ress.split('?')[0]
            # if rss.endswith("css"):
            if type == "":
                name = rss.split('/')[-1]
            elif rss.endswith(type):
                name = rss.split('/')[-1]
            else:
                return content
            name = rss.split('/')[-1]
            url = self.get_content_perfix(ress, domain)
            if url not in self.u_set:
                self.u_set.add(url)
                response = self.get_response(url)
                bytet = response.content
                # 检测关键词
                self.search_key_words(response, name)
                # print("name:%s file_path%s"%(file_path, name))
                self.f_loader(bytet, file_path + name)
                print('已下载', ress)
            path = file_path.split('/')[1]+"/"
            ress = re
            content = re.sub(ress, path + name, content, re.DOTALL)
            print('te-------->', path + name)
        return content

    def filter_scr_name(self, name):
        pass

    def parse_a(self, content, domain):
        res = re.findall('<a.*?href="(.*?)".*?>', content, re.DOTALL)
        return self.parse_core(content, res, "", domain, "html")

    def parse_css(self, content, domain):
        res = re.findall('<link.*?href="(.*?)".*?/>', content, re.DOTALL)
        return self.parse_core(content, res, "css", domain, self.css_path)

    def parse_script(self, content, domain):
        res = re.findall('<script.*?src="(.*?)".*?>', content, re.DOTALL)
        return self.parse_core(content, res, "js", domain, self.js_path)

    def search_key_words(self, content, name=""):
        if self.js_key_words and name.endswith("js"):
            content = content.text
            res = re.findall(self.js_key_words, content, re.DOTALL)
            if res:
                print(len(res), res)
                # print("找到关键词为%s,文件名为%s"%(self.js_key_words, name))
        if self.css_key_words and name.endswith("css"):
            content = content.text
            res = re.findall(self.css_key_words, content)
            if res:
                print("找到关键词为%s,文件名为%s" % (self.css_key_words, name))

    def parse_img(self, content, domain):
        res = re.findall(r'<img.*?src="(.*?)".*?>', content, re.DOTALL)
        return self.parse_core(content, res, "", domain, self.img_path)

    def f_loader(self, content, path):
        paths = path.split("/")
        # print(paths)
        path = os.getcwd() + os.sep + os.sep.join(paths[:-1])
        if not os.path.exists(path):
            os.makedirs(path)
        path += os.sep + paths[-1]
        print(path)
        with open(path, "wb") as f:
            f.write(content)


if __name__ == '__main__':
    spider = MainSpider()
    spider.main(
        'http://www.gsxt.gov.cn/index.html')
    # form_data = {'organId':'100000',
    #     'channelId':'1200'}
    # spider.js_key_words = "infoDetail"
    # spider.main_from_post('http://xwqy.gsxt.gov.cn/mirco/info_list', form_data)
