from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from io import BytesIO
import random

# 绘制随机字符
def generate_random_string(request):
    # 随机字符串
    chars = 'abcdefghijklmnopqrstuvwxyz123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # 随机产生４个不同字符
    random_chars = "".join(random.sample(chars, 4))
    # 随机字符存储到session中
    request.session['verify_code'] = random_chars

    return random_chars


# 获得图片背景颜色
def draw_disturb_point(pen_for_image):
    for _ in range(100):
        # 随机生成干扰点位置
        pos = (random.randint(0, 100), random.randint(0, 30))
        # 随机生成点的颜色
        color = (random.randint(0, 255), 255, random.randint(0, 255))
        # 将点绘制到图片上
        pen_for_image.point(pos, color)


# 给图片绘制随机文字
def draw_random_string(pen_for_image, random_string):
    # 加载字体 字体所在目录:/usr/share/fonts/
    my_font = ImageFont.truetype('FreeMono.ttf', 23)
    # 设置字符颜色
    my_color = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制字符
    for number, ch in enumerate(random_string):
        pen_for_image.text((5 + number * 20, 2), ch, my_color, my_font)


# 绘制基本图片
def create_base_image():
    # 定义图片背景颜色(RGB)
    bg_color = (random.randrange(20, 100), random.randrange(20, 100), 255)
    # 创建图片, 分别设置图片格式, 图片大小, 图片背景颜色
    verify_image = Image.new('RGB', (100, 30), bg_color)

    return verify_image


# 随机图片视图函数
def verification_code(request):
    # 生成随机字符序列
    random_string = generate_random_string(request)
    # 创建图片对象
    verify_image = create_base_image()
    # 创建对图片(verify_image)的画笔
    pen_for_image = ImageDraw.Draw(verify_image)
    # 将随机字符绘制到图片上
    draw_random_string(pen_for_image, random_string)
    # 绘制图片干扰点
    draw_disturb_point(pen_for_image)

    # 将图片数据暂存到内存中
    image_data = BytesIO()
    verify_image.save(image_data, 'png')

    # return HttpResponse(image_data.getvalue(), 'image/png')