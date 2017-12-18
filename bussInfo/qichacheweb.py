import random

import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains



class QchachaWeb:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://www.qichacha.com/user_login")
        WebDriverWait(self.driver, 30).until(
            lambda the_driver: the_driver.find_element_by_xpath('//div[@id="normalLogin"]')
        )
        WebDriverWait(self.driver, 30).until(
            lambda the_driver: the_driver.find_element_by_xpath('//span[@class="nc-lang-cnt"]')
        )
        self.action = ActionChains(self.driver)
        tab = self.driver.find_element_by_xpath('//div[@id="normalLogin"]')
        # time.sleep(2)
        tab.click()


    def get_eles(self):
        self.phone_num_el = self.driver.find_element_by_xpath('//input[@name="nameNormal"]')
        self.pawd_el = self.driver.find_element_by_xpath('//input[@name="pwdNormal"]')
        self.submit_el = self.driver.find_element_by_xpath('//button[@class="btn  btn-primary     m-t-n-xs btn-block btn-lg font-15"]')
        self.slide_el = self.driver.find_element_by_xpath('//span[@class="nc_iconfont btn_slide"]')
        # self.slide_el = self.driver.find_element_by_xpath('//span[@class="nc-lang-cnt"]')
        # self.slide_el = self.driver.find_element_by_xpath('//div[@class="scale_text slidetounlock"]')

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

    @staticmethod
    def sleep_func(length, index):
        mid = length / 2
        if index < mid:
            return abs(mid - index) / 20000
        if index > mid:
            return abs(index - mid) / 22000
        return 0.1

    def input(self, phone_num, pawd):
        self.phone_num_el.send_keys(phone_num)
        self.pawd_el.send_keys(pawd)



    def slide_verify(self):
        slide_location = self.slide_el.location
        slide_y = slide_location['y']
        print("点击滑块")
        # ActionChains(self.driver).click_and_hold(on_element=self.slide_el).perform()
        self.action.move_to_element(self.slide_el).perform()
        self.action.click_and_hold(self.slide_el).perform()
        time.sleep(1)
        print("滑动滑块")
        track_list = self.get_track_list(500)
        for index, track in enumerate(track_list):
            ActionChains(self.driver).move_by_offset(track, 0).perform()
        time.sleep(0.5)
        self.action.release(self.slide_el).perform()
        print("滑块释放")

if __name__ == '__main__':
    web  =QchachaWeb()
    web.get_eles()
    web.input('17349784413', '644973346')
    time.sleep(2)
    web.slide_verify()
    # web.driver.execute_script()