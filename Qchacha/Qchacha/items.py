# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QchachaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 公司名称
    company_name = scrapy.Field()
    # 电话
    company_phone = scrapy.Field()
    # 邮箱
    company_mail = scrapy.Field()
    # 统一社会信用代码
    credit_code = scrapy.Field()
    # 纳税人识别号：
    taxpayer_code = scrapy.Field()
    # 注册号：
    regist_code = scrapy.Field()
    # 组织机构代码：
    org_code = scrapy.Field()
    # 法定代表人
    legal_man = scrapy.Field()
    # 注册资本： registered capital
    registered_capital = scrapy.Field()
    # 经营状态：
    manage_status = scrapy.Field()
    # 成立日期：
    init_date = scrapy.Field()
    # 公司类型：
    company_type = scrapy.Field()
    # 人员规模
    employees = scrapy.Field()
    # 营业期限
    manage_date = scrapy.Field()
    # 登记机关：
    sigind_depa = scrapy.Field()
    # 核准日期：)
    appr_date = scrapy.Field()
    # 英文名
    english_name = scrapy.Field()
    old_name = scrapy.Field()
    # 所属地区
    location = scrapy.Field()
    # 所属行业
    industry = scrapy.Field()
    # 企业地址
    address = scrapy.Field()
    # 经营范围
    business_scope = scrapy.Field()
    # 持股人
    hoder_Main = scrapy.Field()
    # 主要人员
    main_men = scrapy.Field()


class HoderMainItem(scrapy.Item):

    # 持股人名
    name = scrapy.Field()
    # 持股比例
    proportion = scrapy.Field()
    # 资产
    asset = scrapy.Field()
    # 日期
    date = scrapy.Field()
    # 持股类型
    type = scrapy.Field()


class MainManItem(scrapy.Item):

    # 姓名
    name = scrapy.Field()
    # 职务
    posi = scrapy.Field()




class ChangeLogItem(scrapy.Item):

    # 变更日期
    date = scrapy.Field()
    # 变更前
    change_before = scrapy.Field()
    # 变更后
    change_after = scrapy.Field()

