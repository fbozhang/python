# -*- coding:utf-8 -*-
# @Time : 2022/8/26 15:36
# @Author: fbz
# @File : PictureVerificationCode_test.py
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

# # 创建一张图片
# img = Image.new(mode='RGB', size=(120, 30), color=(255, 255, 255))
#
# draw = ImageDraw.Draw(img, mode='RGB')
# font = ImageFont.truetype('Avenus Type.ttf', 30)
# # 写文本
# draw.text([0, 0], 'asd', 'red', font=font)
#
# with open('as.png', 'wb') as f:
#     img.save(f, format='png')


def check_code(width=120, height=30, char_length=5, font_file='Avenus Type.ttf', font_size=28):
    code = []
    img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')

    def rndChar():
        """
        生成随机字母
        :return:
        """
        return chr(random.randint(65, 90))

    def rndColor():
        """
        生成随机颜色
        :return:
        """
        return (random.randint(0, 255), random.randint(10, 255), random.randint(64, 255))

    # 写文字
    font = ImageFont.truetype(font_file, font_size)
    for i in range(char_length):
        char = rndChar()
        code.append(char)
        h = random.randint(0, 4)
        draw.text([i * width / char_length, h], char, font=font, fill=rndColor())

    # 写干扰点
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())

    # 写干扰圆圈
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndColor())

    # 画干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)

        draw.line((x1, y1, x2, y2), fill=rndColor())

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, ''.join(code)


if __name__ == '__main__':
    # 1. 直接打开
    # img,code = check_code()
    # img.show()

    # 2. 写入文件
    img, code = check_code()
    print(img,code)
    with open('as.png', 'wb') as f:
        img.save(f, format='png')

    # 3. 写入内存(Python3)
    # from io import BytesIO
    # stream = BytesIO()
    # img.save(stream, 'png')
    # stream.getvalue()

    # 4. 写入内存（Python2）
    # import StringIO
    # stream = StringIO.StringIO()
    # img.save(stream, 'png')
    # stream.getvalue()

