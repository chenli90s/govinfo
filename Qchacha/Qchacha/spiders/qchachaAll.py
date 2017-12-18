# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Qchacha.items import QchachaItem, MainManItem, HoderMainItem
from scrapy.exceptions import CloseSpider


class QchachaallSpider(CrawlSpider):
    name = 'qchachaAll'
    allowed_domains = ['qichacha.com']
    start_urls = ['http://www.qichacha.com/']

    rules = (
        Rule(LinkExtractor(allow=r'http://www.qichacha.com/gongsi'), follow=True),
        Rule(LinkExtractor(allow=r'http://www.qichacha.com/g_.*?.html'), follow=True),
        Rule(LinkExtractor(allow=r'http://www.qichacha.com/firm_.*?.html'), callback='parse_item',
             follow=False),
        Rule(LinkExtractor(allow=r'http://www.qichacha.com/firm_CN_.*?.html'),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=r'http://www.qichacha.com/gongsi_area.shtml?prov=.*?&p=d+?'),
             follow=True),
    )

    def parse_item(self, response):
        item = QchachaItem()
        try:
            # 公司名称
            item['company_name'] = response.xpath(
                '//*[@id="company-top"]/div/div[1]/span/span/div/div/text()|//*[@id="company-top"]/div/div[2]/div[1]/text()').extract_first().strip()
            # 电话
            phone = response.xpath(
                '//*[@id="company-top"]/div/div[1]/span/small[1]/text()|//*[@id="company-top"]/div/div[2]/div[3]/span[2]/span/text()')
            if phone.extract_first():
                item['company_phone'] = phone.extract_first().strip().split('\t')[-1]

            # 邮箱
            mail = response.xpath(
                '//*[@id="company-top"]/div/div[1]/span/small[1]/a/text()|//*[@id="company-top"]/div/div[2]/div[4]/span[4]/a/text()')
            if mail:
                item['company_mail'] = mail.extract_first().strip()

            # 统一社会信用代码
            item['credit_code'] = response.xpath(
                '//*[@id="Cominfo"]/table/tr[4]/td[4]/text()').extract_first().strip()
            # 纳税人识别号：
            item['taxpayer_code'] = response.xpath(
                '//*[@id="Cominfo"]/table/tr[5]/td[2]/text()').extract_first().strip()
            # 注册号：
            item['regist_code'] = response.xpath(
                '//*[@id="Cominfo"]/table/tr[5]/td[4]/text()').extract_first().strip()
            # 组织机构代码：
            item['org_code'] = response.xpath(
                '//*[@id="Cominfo"]/table/tr[6]/td[2]/text()').extract_first().strip()
            # 法定代表人
            item['legal_man'] = response.xpath(
                '//*[@id="Cominfo"]/table/tr[2]/td[1]/div/div[2]/a[1]/text()').extract_first().strip()
            # 注册资本： registered capital
            item['registered_capital'] = response.xpath(
                '//*[@id="Cominfo"]/table/tr[3]/td[2]/text()').extract_first().strip()
            # 经营状态：
            item['manage_status'] = response.xpath(
                '//*[@id="Cominfo"]/table/tr[4]/td[2]/text()').extract_first().strip()
            # 成立日期：
            item['init_date'] = response.xpath(
                '//*[@id="Cominfo"]/table/tr[3]/td[4]/text()').extract_first().strip()
            # 公司类型：
            item['company_type'] = response.xpath(
                '//*[@id="Cominfo"]/table/tr[6]/td[4]/text()').extract_first().strip()
            # 人员规模
            item['employees'] = response.xpath(
                '//*[@id="Cominfo"]/table/tr[7]/td[2]/text()').extract_first().strip()
            # 营业期限
            item['manage_date'] = response.xpath(
                '//*[@id="Cominfo"]/table/tr[7]/td[4]/text()').extract_first().strip()
            # 登记机关：
            item['sigind_depa'] = response.xpath(
                '//*[@id="Cominfo"]/table/tr[8]/td[2]/text()').extract_first().strip()
            # 核准日期：)
            item['appr_date'] = response.xpath(
                '//*[@id="Cominfo"]/table/tr[8]/td[4]/text()').extract_first().strip()
            # 英文名
            item['english_name'] = response.xpath(
                '//*[@id="Cominfo"]/table/tr[9]/td[2]/text()').extract_first().strip()
            # 曾用名
            item['old_name'] = response.xpath(
                '//*[@id="Cominfo"]/table/tr[9]/td[4]/text()').extract_first().strip()
            # 所属地区
            item['location'] = response.xpath(
                '//*[@id="Cominfo"]/table/tr[10]/td[2]/text()').extract_first().strip()
            # 所属行业
            item['industry'] = response.xpath(
                '//*[@id="Cominfo"]/table/tr[10]/td[4]/text()').extract_first().strip()
            # 企业地址
            item['address'] = response.xpath(
                '//*[@id="Cominfo"]/table/tr[11]/td[2]/text()').extract_first().strip()
            # 经营范围
            item['business_scope'] = response.xpath(
                '//*[@id="Cominfo"]/table/tr[12]/td[2]/text()').extract_first().strip()

            holders = response.xpath('//*[@id="Sockinfo"]/table/tr')
            if holders:
                item['hoder_Main'] = self.parse_holders(holders)
                print("*************************")

            main_men = response.xpath('//*[@id="Mainmember"]/table/tr')

            if main_men:
                item['main_men'] = self.paese_main_men(main_men)
                print("*************************")

            yield item

        except Exception as e:
            # pool = response.request.meta['proxypool']
            # ip_prot = response.request.meta['proxy']
            # pool.gc_ip(ip_prot[2:])
            print("*************************")
            print("**                     **")
            print("**      请求异常        **")
            print("**                     **")
            print("*************************")
            raise CloseSpider('end')
            yield scrapy.Request(response.url, callback=self.parse_item)

    @staticmethod
    def parse_holders(holders):
        holder_item = []
        for index, holder in enumerate(holders):
            if index > 1:
                hitem = HoderMainItem()
                hitem['name'] = holder.xpath('./td[1]/div/a/text()').extract_first()
                hitem['proportion'] = holder.xpath('./td[2]/text()').extract_first().strip()
                hitem['asset'] = holder.xpath('./td[3]/text()').extract_first().strip()
                hitem['date'] = holder.xpath('./td[4]/text()').extract_first().strip()
                hitem['type'] = holder.xpath('./td[5]/text()').extract_first().strip()
                holder_item.append(hitem)
        return holder_item

    @staticmethod
    def paese_main_men(main_men):
        main_mens = []
        for index, main_man in enumerate(main_men):
            if index > 1:
                mitem = MainManItem()
                mitem['name'] = main_man.xpath('./td[1]/div/a/text()').extract_first()
                mitem['posi'] = main_man.xpath('./td[2]/text()').extract_first().strip()
                main_mens.append(mitem)
        return main_mens
