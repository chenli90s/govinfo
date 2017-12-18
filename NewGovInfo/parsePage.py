from lxml import etree
import json


class ParsePage:

    def __init__(self, page_source):
        self.html = etree.HTML(page_source)

    def overview_parse(self, main_info):
        items = main_info[0].xpath('./table[@class="detail-info"]/tr/td')
        # print(items)
        infos = {}
        for item in items:
            title, info = item.xpath('./span/text()')
            # print(title.strip(), info.strip())
            infos[title.strip()] = info.strip()
        return infos

    def parse_main(self):
        """
        照面信息
        :return:
        """
        main_info = self.html.xpath(
            '//div[@class="container1 tabin mainContent printContent"]/div[@class="details clearfix"]/div[@class="overview"]')
        # /html/body/div/div/div/div[2]/div[2]/div[3]/table/tbody/tr[1]/td[1]
        return self.overview_parse(main_info)

    def div_parse(self, items):
        title = items.xpath('./div[2]/table/tr/td[2]/text()')
        if title:
            title = title[0].strip()
            table = items.xpath('./table')
            if table:
                trs = self.parse_table(table[0])
                if trs:
                    return title, trs

    def gen_parse(self):
        """
        通用解析
        :return:
        """
        total_items = self.html.xpath(
            '//div[@class="container1 tabin mainContent printContent"]/div')
        tables = {}
        for items in total_items[1:]:
            # /html/body/div/div/div/div[2]/div[4]/div[2]/table/tbody/tr/td[2]
            res = self.div_parse(items)
            if res:
                tables[res[0]] = res[1]
        return tables

    def parse_table(self, element):
        heads = element.xpath('./thead/tr')
        if heads:
            res = heads[0].xpath('./th/text()')
            heads = res
            trs = element.xpath('./tbody/tr')
            if trs:
                items = []
                for tr in trs:
                    text = tr.xpath('./td/text()')
                    item = {}
                    for index, txt in enumerate(text):
                        item[heads[index].strip()] = txt.strip()
                    items.append(item)
                return items

    def history_parse(self):
        elements = self.html.xpath('//div[@class="mainContent"]/div')
        history = {}
        year_flag = None
        items = {}
        for index, element in enumerate(elements):
            # print(element.attrib)
            if element.attrib and element.attrib.get('class'):
                if year_flag and items:
                    history[year_flag] = items
                    year_flag = None
                    items = {}
                year = elements[index - 1].xpath('./table/tbody/tr/td[2]/text()')
                # print(year, "year_flag")
                year_flag = year[0].strip()
                overview_el = element.xpath('./div[3]/div[@class="overview"]')
                main_info = self.overview_parse(overview_el)
                items["照面信息"] = main_info
            elif not element.attrib:
                # print(element.xpath('./div[2]/table/tr/td[2]/text()'))
                tables = self.div_parse(element)
                if tables:
                    items[tables[0]] = tables[1]
            if len(elements) - 1 == index:
                history[year_flag] = items
        return history

    @staticmethod
    def parse(content):
        parse = ParsePage(content)
        main_info = parse.parse_main()
        res = parse.gen_parse()
        res['照面信息'] = main_info
        history = parse.history_parse()
        res['历史信息'] = history
        res = json.dumps(res, ensure_ascii=False).encode()
        with open('test.json', 'wb') as f:
            f.write(res)


if __name__ == '__main__':
    content = ''
    with open('ttt.html', 'rb') as f:
        # while f.readable():
        content = f.read()
    content = content.decode('gbk')
    parse = ParsePage(content)
    main_info = parse.parse_main()
    res = parse.gen_parse()
    res['照面信息'] = main_info
    history = parse.history_parse()
    res['历史信息'] = history
    res = json.dumps(res, ensure_ascii=False).encode()
    with open('res.json', 'wb') as f:
        f.write(res)
