from PIL import Image
from multiprocessing import Process
import matplotlib.pyplot as plt
import histogram as htg
import aHash as ah
import pHash as ph
import dHash as dh
import sys
import os
import numpy as np

image_01_path='img1.jpg'
image_02_path='img2.jpg'

if __name__ == '__main__':
    print(sys.argv)
    # read image files
    if len(sys.argv)==3:
        img1 = Image.open(os.path.abspath(sys.argv[1]))
        img2 = Image.open(os.path.abspath(sys.argv[2]))
    else:
        img1 = Image.open(image_01_path)
        img2 = Image.open(image_02_path)

    print(np.shape(img1))
    # img1.show()
    # img2.show()

    # Histogram Similarity Calculation
    # regularize the images
    img1_htg = htg.regularizeImage(img1)
    img2_htg = htg.regularizeImage(img2)
    
    hg1 = img1_htg.histogram()
    # print(img1.histogram())
    print('img1的样本点有{}个'.format(len(hg1)))
    hg2 = img2_htg.histogram()
    # print(img2.histogram())
    print('img2的样本点有{}个'.format(len(hg2)))

    # draw the histogram in a no-blocking way
    # sub_thread = Process(target=htg.drawHistogram, args=(hg1, hg2,))
    # sub_thread.start()

    # print the histogram similarity
    print('依据图片直方图距离计算相似度：{}'.format(htg.calMultipleHistogramSimilarity(img1_htg, img2_htg)))

    # aHash Calculation
    print('依据平均哈希算法计算相似度：{}/{}'.format(ah.calaHashSimilarity(img1, img2), 64))

    # pHash Calculation
    print('依据感知哈希算法计算相似度：{}/{}'.format(ph.calpHashSimilarity(img1, img2), 64))

    # dHash Calculation
    print('依据差异哈希算法计算相似度：{}/{}'.format(dh.caldHashSimilarity(img1, img2), 64))

    plt.rcParams['font.sans-serif'] = ['KaiTi']  # 指定默认字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

    plt.figure()
    plt.subplot(2,2,1)
    plt.imshow(img1)
    plt.xticks([])
    plt.yticks([])

    plt.subplot(2,2,3)
    plt.imshow(img2)
    plt.xticks([])
    plt.yticks([])

    plt.subplot(2,2,2)
    plt.plot(range(len(hg1)), hg1, color='blue', linewidth=1.5, label='img1')
    plt.plot(range(len(hg2)), hg2, color='red', linewidth=1.5, label='img2')
    plt.xticks([])
    plt.yticks([])

    string = '依据图片直方图距离计算相似度：\n{}'.format(htg.calMultipleHistogramSimilarity(img1_htg, img2_htg))
    string += '\n\n'
    string += '依据平均哈希算法计算相似度：\n{}/{}'.format(ah.calaHashSimilarity(img1, img2), 64)
    string += '\n\n'
    string += '依据感知哈希算法计算相似度：\n{}/{}'.format(ph.calpHashSimilarity(img1, img2), 64)
    string += '\n\n'
    string += '依据差异哈希算法计算相似度：\n{}/{}'.format(dh.caldHashSimilarity(img1, img2), 64)

    plt.subplot(2, 2, 4)
    plt.text(0.05, 0.05, string)
    plt.xticks([])
    plt.yticks([])

    plt.show()
