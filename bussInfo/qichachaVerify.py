import random
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import base64
from PIL import Image, ImageDraw, ImageFont
import os
from damatuWeb import DamatuApi


class QchachaVerify:

    def __init__(self, url):
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        WebDriverWait(self.driver, 30).until(
            lambda the_driver: the_driver.find_element_by_xpath('//*[@id="nc_1__scale_text"]/span')
        )
        self.action = ActionChains(self.driver)
        time.sleep(1)

    @staticmethod
    def get_track_list(distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 2
            else:
                # 加速度为负3
                a = -3
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
    # def get_track_list(length):
    #     track_list = []
    #     # length += 10
    #     x = random.randint(2, 4)
    #     while length - x >= 6:
    #         track_list.append(x)
    #         length = length - x
    #         x = random.randint(2, 4)
    #     # for i in range(length):
    #     for j in range(length):
    #         track_list.append(1)
    #     return track_list

    @staticmethod
    def sleep_func(length, index):
        mid = length / 2
        if index < mid:
            return abs(mid - index) / 2000
        if index > mid:
            return abs(index - mid) / 2200
        return 0.1

    def slide_squ(self):
        time.sleep(3)
        squ_el = self.driver.find_element_by_xpath('//*[@id="nc_1_n1z"]')
        self.action.move_to_element(squ_el).perform()
        self.action.click_and_hold(squ_el).perform()
        track_list = self.get_track_list(303)
        time.sleep(1)
        for index, track in enumerate(track_list):
            ActionChains(self.driver).move_by_offset(track, 0).perform()
        time.sleep(1)
        self.action.release(squ_el)
        print('完成滑动')
        res = self.img_verify()
        # while not res:
        #     res = self.img_verify()
        # btn = self.driver.find_element_by_xpath('//*[@id="verify"]')
        # btn.click()

    def get_con_img(self, question, verify_img_name):
        verify_img = Image.open(verify_img_name)
        img = Image.new('RGB', (200, 230), (255, 255, 255))
        draw_img = ImageDraw.Draw(img)
        font = ImageFont.truetype('msyhsl.ttc', 18)
        draw_img.text((2, 2), question, (0, 0, 0), font)
        img.paste(verify_img, (0, 30))
        img.save('test.jpg')
        os.remove(os.path.join(os.getcwd(), verify_img_name))
        pos = self.api_get_res('test.jpg')
        # os.remove(os.path.join(os.getcwd(), 'test.jpg'))
        return pos

    def api_get_res(self, img_name):
        api = DamatuApi('test', 'test')
        print("余额为：%s" % api.getBalance())
        pos = api.decode(img_name, 285)
        print(pos)
        return pos

    def click_img(self, pos):
        script = """
                
                function imitateClick(oElement, x, y) {
                var oEvent;
            
                oEvent = document.createEvent('MouseEvents');
                oEvent.initEvent('click', true, true, document.defaultView, 0, 0, 0, x, y);
                oElement.dispatchEvent(oEvent);
                }

                divImgEls = document.getElementsByClassName('clickCaptcha_img')
                divImgEl = divImgEls[0]
                imgEl = divImgEl.firstChild
                imitateClick(imgEl, %s, %s);
                """
        pos = pos.split(",")
        img_el = self.driver.find_element_by_xpath('//*[@id="nc_1_clickCaptcha"]/div[2]/img')
        locations = img_el.location
        size = img_el.size
        print(locations, size)
        x_pre = size['width']/200
        pos = int(pos[0])*x_pre, (int(pos[1])-30)*x_pre
        pos = locations['x']+pos[0], locations['y']+pos[1]
        print(pos)
        script = script%(str(pos[0]), str(pos[1]))
        print(script)
        # self.driver.execute_script(script)

    def img_verify(self):
        # try:
        WebDriverWait(self.driver, 30).until(
            lambda the_driver: the_driver.find_element_by_xpath(
                '//*[@id="nc_1_clickCaptcha"]/div[2]/img')
        )
        img_base_code = self.driver.find_element_by_xpath('//*[@id="nc_1_clickCaptcha"]/div[2]/img')
        img_base_code = img_base_code.get_attribute("src")
        img_bt = base64.b64decode(img_base_code.split(',')[1])
        with open('test1.jpg', 'wb') as f:
            f.write(img_bt)
        questions = self.driver.find_element_by_xpath('//*[@id="nc_1__scale_text"]')
        questions = questions.text
        print(questions)
        pos = self.get_con_img(questions, 'test1.jpg')
        self.driver.save_screenshot('srceenl.jpg')
        self.click_img(pos)
        # try:
        #     res = self.driver.find_element_by_xpath('//*[@id="nc_1__scale_text"]/span/b')
        #     str = res.text
        #     if str == '验证通过':
        #         return True
        # # time.sleep(3)
        # except Exception as e:
        #     print(e)


if __name__ == '__main__':
    web = QchachaVerify(
        'http://www.qichacha.com/index_verify?type=companyview&back=/firm_8f9d4a6c2bcce9becb380ddf0d9786a9.html')
    web.slide_squ()
