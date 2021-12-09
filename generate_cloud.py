# -*- coding: utf-8 -*-
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import jieba
from wordcloud import ImageColorGenerator

manpngpath = "E:\\ZhuhuPJ2\\man\\man.png"
womanpngpath = "E:\\ZhuhuPJ2\\woman\\woman.png"
womantext = "E:\\ZhuhuPJ2\\woman\\women_all.txt"
mantext = "E:\\ZhuhuPJ2\\man\\men_all.txt"
fontpath = "E:\\ZhuhuPJ2\\kai.ttf"
store_path_man = "E:\\ZhuhuPJ2\\man\\man_result.png"
store_path_woman = "E:\\ZhuhuPJ2\\woman\\woman_result.png"

# 打开文本
text = open(womantext,"r",encoding = "utf-8").read()
pngpath_color = np.array(Image.open(womanpngpath))
# 中文分词
text = ' '.join(jieba.cut(text))
print(text[:100])

image_colors = ImageColorGenerator(pngpath_color)
 
# 生成对象
mask = np.array(Image.open(womanpngpath))
wc = WordCloud(mask=mask, font_path=fontpath, mode='RGBA', background_color=None).generate(text)
 
# 显示词云
plt.imshow(wc.recolor(color_func = image_colors), interpolation='bilinear')
plt.axis("off")
plt.show()
 
# 保存到文件
wc.to_file(store_path_woman)
