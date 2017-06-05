# 抓取弹幕后保存为text文档，然后词云分析,此部分是词云部分
__author__ = '布咯咯_rieuse'
__time__ = '2017.6.2'
__github__ = 'https://github.com/rieuse'

import jieba
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import os
import PIL.Image as Image
import numpy as np

with open('大司马上课后.txt', 'r', encoding='utf-8') as f:
    text = f.read()
    f.close()
cut_text = " ".join(jieba.cut(text))

d = os.path.dirname(__file__)
color_mask = np.array(Image.open(os.path.join(d, 'img.jpg')))
my_wordcloud = WordCloud(
    background_color='#F0F8FF',  # 背景颜色
    font_path="FZLTKHK--GBK1-0.ttf",  # 使用特殊字体可以显示中文
    max_words=8000,
    font_step=20,  # 步调太大，显示的词语就少了
    mask=color_mask,
    random_state=15,  # 设置有多少种随机生成状态，即有多少种配色方案
    min_font_size=15,
    max_font_size=202,
)
my_wordcloud.generate(cut_text)
image_colors = ImageColorGenerator(color_mask)
plt.show(my_wordcloud.recolor(color_func=image_colors))
plt.imshow(my_wordcloud)  # 以图片的形式显示词云
plt.axis('off')  # 关闭坐标轴
plt.show()  # 展示图片

my_wordcloud.to_file(os.path.join(d, 'pic.jpg'))
