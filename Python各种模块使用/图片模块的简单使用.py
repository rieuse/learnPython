from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import numpy as np
'''一：打开显示保存'''

# img = Image.open('img/3.jpg')
# plt.figure('meizi')
# plt.imshow(img)
# plt.axis('off')
# plt.show()


'''二.图像通道几何变换裁剪'''

# img = Image.open('img/3.jpg')
# img的属性信息
# print(img.size)
# print(img.mode)
# print(img.format)

# 简单保存，可以通史转换图片的格式
# img.save('img/text.png')

# 彩色图像转灰度图
# gr = img.convert('L')
# plt.figure("meizi")
# plt.imshow(gr,cmap='gray')
# plt.axis('off')
# plt.show()

'''
使用函数convert()来进行转换，它是图像实例对象的一个方法，接受一个 mode 参数，用以指定一种色彩模式，mode 的取值可以是如下几种：
· 1 (1-bit pixels, black and white, stored with one pixel per byte)
· L (8-bit pixels, black and white)
· P (8-bit pixels, mapped to any other mode using a colour palette)
· RGB (3x8-bit pixels, true colour)
· RGBA (4x8-bit pixels, true colour with transparency mask)
· CMYK (4x8-bit pixels, colour separation)
· YCbCr (3x8-bit pixels, colour video format)
· I (32-bit signed integer pixels)
· F (32-bit floating point pixels)
'''
# 通道分离与合并

# img = Image.open('img/3.jpg')
# gray = img.convert('L') #转换成灰度
# r,g,b = img.split()     #分离三通道
# pic =  Image.merge('RGB',(r,g,b))  #合并三通道
# plt.figure("beauty")
# plt.subplot(2,3,1), plt.title('origin')
# plt.imshow(img),plt.axis('off')
# plt.subplot(2,3,2), plt.title('gray')
# plt.imshow(gray,cmap='gray'),plt.axis('off')
# plt.subplot(2,3,3), plt.title('merge')
# plt.imshow(pic),plt.axis('off')
# plt.subplot(2,3,4), plt.title('r')
# plt.imshow(r,cmap='gray'),plt.axis('off')
# plt.subplot(2,3,5), plt.title('g')
# plt.imshow(g,cmap='gray'),plt.axis('off')
# plt.subplot(2,3,6), plt.title('b')
# plt.imshow(b,cmap='gray'),plt.axis('off')
# plt.show()

# 裁剪图片
# img = Image.open('img/3.jpg')
# plt.figure("beauty")
# plt.subplot(1,2,1),plt.title('origin')
# plt.imshow(img),plt.axis('off')
#
# box=(180,100,400,300)
# plt.subplot(1,2,2),plt.title('after')
# plt.imshow(img.crop(box)),plt.axis('off')
# plt.show()

# 几何变换
# Image类有resize()、rotate()、transpose()方法进行几何变换
# 1.图像的缩放和旋转
# img = Image.open('img/3.jpg')
# dst1 = img.resize((128,228))
# dst2 = img.rotate(45)   #顺时针角度表示
# plt.figure('meizi')
# plt.subplot(1,3,1), plt.title('origin')
# plt.imshow(img),plt.axis('off')
# plt.subplot(1,3,2), plt.title('Scale')
# plt.imshow(dst1),plt.axis('off')
# plt.subplot(1,3,3), plt.title('rotate')
# plt.imshow(dst2),plt.axis('off')
# plt.show()

# 2.转换图像
# #transpose()和rotate()没有性能差别

# img = Image.open('img/3.jpg')
# dst1 = img.transpose(Image.FLIP_LEFT_RIGHT)   #左右互换
# dst2 = img.transpose(Image.FLIP_TOP_BOTTOM)   #上下互换
# dst3 = img.transpose(Image.ROTATE_90)     #顺时针旋转
# dst4 = img.transpose(Image.ROTATE_180)
# dst5 = img.transpose(Image.ROTATE_270)
# plt.subplot(2,3,1)
# plt.imshow(img),plt.axis('off')
# plt.subplot(2,3,2)
# plt.imshow(dst1),plt.axis('off')
# plt.subplot(2,3,3)
# plt.imshow(dst2),plt.axis('off')
# plt.subplot(2,3,4)
# plt.imshow(dst3),plt.axis('off')
# plt.subplot(2,3,5)
# plt.imshow(dst4),plt.axis('off')
# plt.subplot(2,3,6)
# plt.imshow(dst5),plt.axis('off')
# plt.show()

'''三. 添加水印'''

# 添加文字水印
# im = Image.open('img/3.jpg')
# font = ImageFont.truetype("方正准圆简体.ttf", 48)
# draw = ImageDraw.Draw(im)
# draw.text((10, 10), '漂亮的妹子', fill=(255, 0, 0), font=font)  # fill 为rgb颜色 font设置字体
# plt.imshow(im)
# plt.axis('off')
# plt.show()


# 添加小图片水印
# im = Image.open('img/3.jpg')
# mark=Image.open('img/jiayou.png')
# layer=Image.new('RGBA',im.size,(0,0,0,0))
# layer.paste(mark,(im.size[0]-200,im.size[1]-200))
# outimg=Image.composite(layer,im,layer)
# plt.imshow(outimg)
# plt.axis('off')
# plt.show()
