from driverSpiderPrint import WebSpider, WebDriverPrint
from parsePageVersion2 import ParsePageV2
import random

f = open('link.txt', 'w')

ver = [ '搜狐', '新浪', '腾讯', "百度", "阿里巴巴"]
def query_code(item):
    print(item[0], item[1])
    f.write(item[1]+'\n')
    return True

def main():
    # for v in ver:
    links = WebSpider.verify_main(random.choice(ver), query_code)
    for link in links:
        res = WebDriverPrint.verify_main(link)
        try:
            ParsePageV2.parse(res)
        except Exception as e:
            print(e)
    f.close()

if __name__ == '__main__':
    main()
    # links = WebSpider.verify_main('搜狐', query_code)