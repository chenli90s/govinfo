from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import requests
import agent as agent
import random
import PIL.Image as image
import os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class WebSpider:

    domain = 'http://www.gsxt.gov.cn'

    def __init__(self, keywords, tools):
        # dcap = dict(DesiredCapabilities.PHANTOMJS)
        # dcap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
        # self.driver = webdriver.PhantomJS(desired_capabilities=dcap)
        self.tools = tools
        self.driver = webdriver.Chrome()
        self.driver.get('http://www.gsxt.gov.cn/index.html')
        WebDriverWait(self.driver, 30).until(
            lambda the_driver: the_driver.find_element_by_xpath('//*[@id="keyword"]'))
        WebDriverWait(self.driver, 30).until(
            lambda the_driver: the_driver.find_element_by_xpath('//*[@id="btn_query"]'))
        self.btn_el = self.driver.find_element_by_id('btn_query')
        self.input_el = self.driver.find_element_by_id('keyword')
        time.sleep(3)
        self.input_el.clear()
        self.input_el.send_keys(keywords)
        self.btn_el.click()
        # self.slide_el.click()
        self.action = ActionChains(self.driver)

    def get_image(self, xpath):
        # //div[@class="gt_cut_fullbg_slice"]
        img_el = self.driver.find_elements_by_xpath(xpath)
        location_list = []
        imageurl = ''
        for background_image in img_el:
            location = {}
            location['x'] = int(
                re.findall("background-image: url\(\"(.*)\"\); background-position: (.*)px (.*)px;",
                           background_image.get_attribute('style'))[0][1])
            location['y'] = int(
                re.findall("background-image: url\(\"(.*)\"\); background-position: (.*)px (.*)px;",
                           background_image.get_attribute('style'))[0][2])
            if not imageurl:
                imageurl = \
                    re.findall(
                        "background-image: url\(\"(.*)\"\); background-position: (.*)px (.*)px;",
                        background_image.get_attribute('style'))[0][0]
            location_list.append(location)
        imageurl = imageurl.replace("webp", "jpg")
        response = requests.get(imageurl, headers=dict(Agent=random.choice(agent.agents)))
        if response.status_code == 200:
            with open(imageurl.split("/")[-1], 'wb') as f:
                f.write(response.content)
        # 合并图片
        img = self.get_merge_image(imageurl.split('/')[-1], location_list)
        os.remove(os.path.join(os.getcwd(), imageurl.split("/")[-1]))
        return img

    def get_merge_image(self, filename, location_list):
        im = image.open(filename)
        im_list_upper = []
        im_list_down = []
        for location in location_list:
            if location['y'] == -58:
                im_list_upper.append(
                    im.crop((abs(location['x']), 58, abs(location['x']) + 10, 166)))
            if location['y'] == 0:
                im_list_down.append(im.crop((abs(location['x']), 0, abs(location['x']) + 10, 58)))
        new_im = image.new('RGB', (260, 116))
        x_offset = 0
        for im in im_list_upper:
            new_im.paste(im, (x_offset, 0))
            x_offset += im.size[0]
        x_offset = 0
        for im in im_list_down:
            new_im.paste(im, (x_offset, 58))
            x_offset += im.size[0]
        # new_im.save('new_%s.jpg' % filename)
        return new_im

    @staticmethod
    def is_similar(img1, img2, x, y):
        pixel1 = img1.getpixel((x, y))
        pixel2 = img2.getpixel((x, y))
        for i in range(0, 3):
            if abs(pixel1[i] - pixel2[i]) >= 50:
                return False
        return True

    @staticmethod
    def get_diff_location(img1, img2):
        for i in range(0, 260):
            for j in range(0, 116):
                if not WebSpider.is_similar(img1, img2, i, j):
                    return i

    @staticmethod
    def get_track(distance):
        """
                根据偏移量获取移动轨迹
                :param distance: 偏移量
                :return: 移动轨迹
                """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        geet = random.randint(3, 6)
        # 减速阈值
        mid = distance * geet / geet + 1
        # 计算间隔
        tv = random.randint(10, 20)
        t = tv / 100
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 2
            else:
                # 加速度为负3
                a = -4
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track

    # @staticmethod
    # def get_track(distance):
    #     """
    #     根据偏移量获取移动轨迹
    #     :param distance: 偏移量
    #     :return: 移动轨迹
    #     """
    #     # 移动轨迹
    #     track = []
    #     # 当前位移
    #     current = 0
    #     # 减速阈值
    #     mid = distance * 4 / 5
    #     # 计算间隔
    #     t = 0.2
    #     # 初速度
    #     v = 0
    #
    #     while current < distance:
    #         if current < mid:
    #             # 加速度为正2
    #             a = 2
    #         else:
    #             # 加速度为负3
    #             a = -3
    #         # 初速度v0
    #         v0 = v
    #         # 当前速度v = v0 + at
    #         v = v0 + a * t
    #         # 移动距离x = v0t + 1/2 * a * t^2
    #         move = v0 * t + 1 / 2 * a * t * t
    #         # 当前位移
    #         current += move
    #         # 加入轨迹
    #         track.append(round(move))
    #     return track

    @staticmethod
    def sleep_func(length, index):
        mid = length / 2
        if index < mid:
            return abs(mid - index) / 500
        if index > mid:
            return abs(index - mid) / 500
        return 0.1

    def back_ball(self, ball_el, ball_y):
        self.action.move_to_element_with_offset(to_element=ball_el, xoffset=21,
                                                yoffset=random.randint(-3, 3)).perform()
        time.sleep(random.randint(10, 50) / 200)

    def move_to(self, ball_el, track_list):
        # 点击圆球
        # print("点击小球", ball_el)
        self.action.move_to_element(ball_el).perform()
        self.action.click_and_hold(on_element=ball_el).perform()
        time.sleep(1)
        # print("滑动小球", track_list)
        for index, track in enumerate(track_list):
            track_str = "{%d,%d}" % (track, 0)
            ActionChains(self.driver).move_by_offset(track, 0).perform()
            # print(track_str)

        time.sleep(0.5)
        # for i in range(5):
        #     self.back_ball(ball_el, 0)
        # print("第三步，释放鼠标")
        self.action.release(on_element=ball_el).perform()
        WebDriverWait(self.driver, 10).until(
            lambda the_driver: the_driver.find_element_by_xpath('//div[@class="gt_info_text"]')
        )

    def slider_ball(self, loc):
        track_list = self.get_track(loc - 5)
        WebDriverWait(self.driver, 10).until(
            lambda the_driver: the_driver.find_element_by_xpath(
                '//div[@class="gt_slider_knob gt_show"]')
        )
        ball_el = self.driver.find_element_by_xpath('//div[@class="gt_slider_knob gt_show"]')
        # print(loc)
        self.move_to(ball_el, track_list)

    def parse_link(self):
        WebDriverWait(self.driver, 30).until(
            lambda the_driver: the_driver.find_elements_by_xpath(
                '//a[@class="search_list_item db"]')
        )
        links = self.driver.find_elements_by_xpath('//a[@class="search_list_item db"]')
        res_links = []
        for link in links:
            code = link.find_element_by_xpath('//div[@class="div-map2"]/span')
            if self.tools((code.text, link.get_attribute('href'))):
                res_links.append(link.get_attribute('href'))
        return res_links

    def get_list_link(self):
        links = []
        links.extend(self.parse_link())
        el_link = True
        while el_link:
            el_link = self.driver.find_elements_by_xpath('//form/a')
            # print(el_link[-2].text)
            if el_link and el_link[-2].text == '下一页':
                # self.driver.find_elements_by_xpath("//from")
                el_link[-2].click()
                links.extend(self.parse_link())
                time.sleep(5)
            else:
                el_link = False
        return links

    def slide_verify(self):
        img1 = self.get_image('//div[@class="gt_cut_bg_slice"]')
        img2 = self.get_image('//div[@class="gt_cut_fullbg_slice"]')
        loc = self.get_diff_location(img1, img2)
        # print("length-------%d"%loc)
        self.slider_ball(loc)
        time.sleep(3)
        try:
            WebDriverWait(self.driver, 10).until(
                lambda the_driver: the_driver.find_element_by_xpath('//div[@class="search_result"]')
            )
            res = self.driver.find_element_by_xpath('//div[@class="search_result"]')
            self.links = self.get_list_link()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def verify_main(keywords, tools):
        web = None
        flag = False
        count = 0
        while not flag:
            del web
            try:
                web = WebSpider(keywords, tools)
                flag = web.slide_verify()
                count += 1
            except Exception as e:
                web = None
                print('出错了', e)

        return web.links

    def __del__(self):
        if self.driver:
            self.driver.close()


if __name__ == '__main__':
    links = WebSpider.verify_main("中国移动")
    print(links)
    print(len(links))
