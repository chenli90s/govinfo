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
        time.sleep(1)
        self.print_el = self.driver.find_element_by_xpath('//*[@id="btn_print"]')
        self.action = ActionChains(self.driver)
        # self.scroll_page()
        self.to_print_init()

    def scroll_page(self):
        loadmore = self.driver.find_element_by_xpath('//div[@id="addmore"]')
        gone = loadmore.get_attribute('style')
        print(gone)
        while 'block' in gone:
            self.driver.execute_script('clickToAddmore()')
            print("moving", gone)
            time.sleep(3)
            gone = loadmore.get_attribute('style')
        print(self.driver.page_source, gone)

    def to_print_init(self):
        self.print_el.click()
        WebDriverWait(self.driver, 30).until(
            lambda the_driver: the_driver.find_elements_by_xpath(
                '//div[@class="gt_holder gt_popup gt_show"]/div[2]/div[2]/div[1]/div[2]/div[1]/a[1]/div[1]/div')
        )
        WebDriverWait(self.driver, 30).until(
            lambda the_driver: the_driver.find_elements_by_xpath(
                '//div[@class="gt_holder gt_popup gt_show"]/div[2]/div[2]/div[1]/div[2]/div[1]/a[2]/div[1]/div')

        )

    def slider_ball(self, loc):
        track_list = self.get_track(loc - 6)
        ball_el = self.driver.find_element_by_xpath(
            '//div[@class="gt_holder gt_popup gt_show"]/div[2]/div[2]/div[2]/div[@class="gt_slider_knob gt_show"]')
        # print(loc)
        self.move_to(ball_el, track_list)

    def slide_verify(self):
        img1 = self.get_image(
            '//div[@class="gt_holder gt_popup gt_show"]/div[2]/div[2]/div[1]/div[2]/div[1]/a[1]/div[1]/div')
        img2 = self.get_image(
            '//div[@class="gt_holder gt_popup gt_show"]/div[2]/div[2]/div[1]/div[2]/div[1]/a[2]/div[1]/div')
        loc = self.get_diff_location(img1, img2)
        self.slider_ball(loc)
        time.sleep(5)
        try:
            WebDriverWait(self.driver, 10).until(
                lambda the_driver: the_driver.find_element_by_xpath(
                    '//div[@class="container1 tabin mainContent printContent"]')
            )
            res = self.driver.find_element_by_xpath(
                '//div[@class="container1 tabin mainContent printContent"]')
            return True
        except:
            WebDriverWait(self.driver, 10).until(
                lambda the_driver: the_driver.find_element_by_xpath('//div[@class="gt_info_text"]')
            )
            print(self.driver.find_element_by_xpath('//div[@class="gt_info_text"]').text)
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
                time.sleep(10)
            except:
                web = None
                print('出错了')
        return web.driver.page_source


if __name__ == '__main__':
    page = WebDriverPrint.verify_main(
        'http://www.gsxt.gov.cn/%7BVoy0CUVVrowCXyCo9DOiar_FtKOxS055VbQBG_CEbEnWHlm-XkMcOwQKq4n8mQWB1hMw3dchKvAr_gxHsZLyfn3L_wOKFyaNOEJqVuf6v1ZyqNCV7-74NrCeSmS_hkRe-1513559970813%7D'
    )
    with open("ttt.html", 'w') as f:
        f.write(page)
    # from parsePage import ParsePage
    #
    # ParsePage.parse(page)
