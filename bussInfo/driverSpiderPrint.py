from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time
from driverSpider import WebSpider


class WebDriverPrint(WebSpider):


    def __init__(self, url):
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        WebDriverWait(self.driver, 30).until(
            lambda the_driver: the_driver.find_element_by_xpath('//*[@id="btn_print"]')
        )
        time.sleep(3)
        self.print_el = self.driver.find_element_by_xpath('//*[@id="btn_print"]')
        self.print_el.click()
        self.action = ActionChains(self.driver)
        WebDriverWait(self.driver, 30).until(
            lambda the_driver: the_driver.find_elements_by_xpath('//div[@class="gt_holder gt_popup gt_show"]/div[2]/div[2]/div[1]/div[2]/div[1]/a[1]/div[1]/div')
        )
        WebDriverWait(self.driver, 30).until(
            lambda the_driver: the_driver.find_elements_by_xpath(
                '//div[@class="gt_holder gt_popup gt_show"]/div[2]/div[2]/div[1]/div[2]/div[1]/a[2]/div[1]/div')

        )


    def slider_ball(self, loc):
        track_list = self.get_track(loc - 6)
        ball_el = self.driver.find_element_by_xpath('//div[@class="gt_holder gt_popup gt_show"]/div[2]/div[2]/div[2]/div[@class="gt_slider_knob gt_show"]')
        # print(loc)
        self.move_to(ball_el, track_list)

    def slide_verify(self):
        img1 = self.get_image('//div[@class="gt_holder gt_popup gt_show"]/div[2]/div[2]/div[1]/div[2]/div[1]/a[1]/div[1]/div')
        img2 = self.get_image('//div[@class="gt_holder gt_popup gt_show"]/div[2]/div[2]/div[1]/div[2]/div[1]/a[2]/div[1]/div')
        loc = self.get_diff_location(img1, img2)
        self.slider_ball(loc)
        time.sleep(5)
        try:
            res = self.driver.find_element_by_xpath('/html/body/div/div/div/div[2]')
            return True
        except:
            # print("被吃掉了")
            return False

    @staticmethod
    def verify_main(url=""):
        web = None
        flag = False
        count = 0
        while not flag:
            del web
            try:
                web = WebDriverPrint(url)
                flag = web.slide_verify()
                count += 1
            except:
                print('出错了')
        return web.driver.page_source


if __name__ == '__main__':
    page = WebDriverPrint.verify_main('http://www.gsxt.gov.cn/%7BpTUUbd4LIE60CpWUJLc0WGd_VS6tVkJOiMQmBgUs5fdg5vGm0HOYPJYTJQZMVL6RQQUUIc_vXzkcmh0ePCc6EpII5vSe2eprYNt6A3yBWcUCUZghF1mnMa9WRTiHKqbCNfMcaowkOBFOZmk7XEKjow-1512967496525%7D')
    print(page)