from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import PIL.Image as image
import time,re, random
import requests

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

#爬虫模拟的浏览器头部信息
agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
headers = {
        'User-Agent': agent
        }

# 根据位置对图片进行合并还原
# filename:图片
# location_list:图片位置
#内部两个图片处理函数的介绍
#crop函数带的参数为(起始点的横坐标，起始点的纵坐标，宽度，高度）
#paste函数的参数为(需要修改的图片，粘贴的起始点的横坐标，粘贴的起始点的纵坐标）
def get_merge_image(filename,location_list):
    #打开图片文件
    im = image.open(filename)
    #创建新的图片,大小为260*116
    new_im = image.new('RGB', (260,116))
    im_list_upper=[]
    im_list_down=[]
    # 拷贝图片
    for location in location_list:
        #上面的图片
        if location['y']==-58:
            im_list_upper.append(im.crop((abs(location['x']),58,abs(location['x'])+10,166)))
        #下面的图片
        if location['y']==0:
            im_list_down.append(im.crop((abs(location['x']),0,abs(location['x'])+10,58)))
    new_im = image.new('RGB', (260,116))
    x_offset = 0
    #黏贴图片
    for im in im_list_upper:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]
    x_offset = 0
    for im in im_list_down:
        new_im.paste(im, (x_offset,58))
        x_offset += im.size[0]
    return new_im

#下载并还原图片
# driver:webdriver
# div:图片的div
def get_image(driver,div):
    #找到图片所在的div
    background_images=driver.find_elements_by_xpath(div)
    location_list=[]
    imageurl=''
    #图片是被CSS按照位移的方式打乱的,我们需要找出这些位移,为后续还原做好准备
    for background_image in background_images:
        location={}
        #在html里面解析出小图片的url地址，还有长高的数值
        location['x']=int(re.findall("background-image: url\(\"(.*)\"\); background-position: (.*)px (.*)px;",background_image.get_attribute('style'))[0][1])
        location['y']=int(re.findall("background-image: url\(\"(.*)\"\); background-position: (.*)px (.*)px;",background_image.get_attribute('style'))[0][2])
        imageurl=re.findall("background-image: url\(\"(.*)\"\); background-position: (.*)px (.*)px;",background_image.get_attribute('style'))[0][0]
        location_list.append(location)
    #替换图片的后缀,获得图片的URL
    imageurl=imageurl.replace("webp","jpg")
    #获得图片的名字
    imageName = imageurl.split('/')[-1]
    #获得图片
    session = requests.session()
    r = session.get(imageurl, headers = headers, verify = False)
    #下载图片
    with open(imageName, 'wb') as f:
        f.write(r.content)
        f.close()
    #重新合并还原图片
    image=get_merge_image(imageName, location_list)
    return image

#对比RGB值
def is_similar(image1,image2,x,y):
    pass
    #获取指定位置的RGB值
    pixel1=image1.getpixel((x,y))
    pixel2=image2.getpixel((x,y))
    for i in range(0,3):
        # 如果相差超过50则就认为找到了缺口的位置
        if abs(pixel1[i]-pixel2[i])>=50:
            return False
    return True

#计算缺口的位置
def get_diff_location(image1,image2):
    i=0
    # 两张原始图的大小都是相同的260*116
    # 那就通过两个for循环依次对比每个像素点的RGB值
    # 如果相差超过50则就认为找到了缺口的位置
    for i in range(0,260):
        for j in range(0,116):
            if is_similar(image1,image2,i,j)==False:
                return  i

#根据缺口的位置模拟x轴移动的轨迹
def get_track(length):
    pass
    list=[]
    #间隔通过随机范围函数来获得,每次移动一步或者两步
    x=random.randint(1,3)
    #生成轨迹并保存到list内
    while length-x>=5:
        list.append(x)
        length=length-x
        x=random.randint(1,3)
    #最后五步都是一步步移动
    for i in range(length):
        list.append(1)
    return list

#滑动验证码破解程序
def main():
    #打开chrome浏览器
    driver = webdriver.Chrome()
    #用chrome浏览器打开网页
    driver.get("http://www.geetest.com/exp_embed")
    #等待页面的上元素刷新出来
    WebDriverWait(driver, 30).until(lambda the_driver: the_driver.find_element_by_xpath("//div[@class='gt_slider_knob gt_show']").is_displayed())
    WebDriverWait(driver, 30).until(lambda the_driver: the_driver.find_element_by_xpath("//div[@class='gt_cut_bg gt_show']").is_displayed())
    WebDriverWait(driver, 30).until(lambda the_driver: the_driver.find_element_by_xpath("//div[@class='gt_cut_fullbg gt_show']").is_displayed())
    #下载图片
    image1=get_image(driver, "//div[@class='gt_cut_bg gt_show']/div")
    image2=get_image(driver, "//div[@class='gt_cut_fullbg gt_show']/div")
    #计算缺口位置
    loc=get_diff_location(image1, image2)
    #生成x的移动轨迹点
    track_list=get_track(loc)
    #找到滑动的圆球
    element=driver.find_element_by_xpath("//div[@class='gt_slider_knob gt_show']")
    location=element.location
    #获得滑动圆球的高度
    y=location['y']
    #鼠标点击元素并按住不放
    print ("第一步,点击元素")
    ActionChains(driver).click_and_hold(on_element=element).perform()
    time.sleep(0.15)
    print ("第二步，拖动元素")
    track_string = ""
    for track in track_list:
        #不能移动太快,否则会被认为是程序执行
        track_string = track_string + "{%d,%d}," % (track, y - 445)
        #xoffset=track+22:这里的移动位置的值是相对于滑动圆球左上角的相对值，而轨迹变量里的是圆球的中心点，所以要加上圆球长度的一半。
        #yoffset=y-445:这里也是一样的。不过要注意的是不同的浏览器渲染出来的结果是不一样的，要保证最终的计算后的值是22，也就是圆球高度的一半
        ActionChains(driver).move_to_element_with_offset(to_element=element, xoffset=track+22, yoffset=y-445).perform()
        #间隔时间也通过随机函数来获得,间隔不能太快,否则会被认为是程序执行
        time.sleep(random.randint(10,50)/100)
    print (track_string)
    #xoffset=21，本质就是向后退一格。这里退了5格是因为圆球的位置和滑动条的左边缘有5格的距离
    ActionChains(driver).move_to_element_with_offset(to_element=element, xoffset=21, yoffset=y-445).perform()
    time.sleep(0.1)
    ActionChains(driver).move_to_element_with_offset(to_element=element, xoffset=21, yoffset=y-445).perform()
    time.sleep(0.1)
    ActionChains(driver).move_to_element_with_offset(to_element=element, xoffset=21, yoffset=y-445).perform()
    time.sleep(0.1)
    ActionChains(driver).move_to_element_with_offset(to_element=element, xoffset=21, yoffset=y-445).perform()
    time.sleep(0.1)
    ActionChains(driver).move_to_element_with_offset(to_element=element, xoffset=21, yoffset=y-445).perform()
    print ("第三步，释放鼠标")
    #释放鼠标
    ActionChains(driver).release(on_element=element).perform()
    time.sleep(3)
    #点击验证
    # submit = driver.find_element_by_xpath("//div[@class='gt_ajax_tip success']")
    # print(submit.location)
    # time.sleep(5)
    #关闭浏览器,为了演示方便,暂时注释掉.
    #driver.quit()

#主函数入口
if __name__ == '__main__':
    pass
    main()


