from PIL import Image
from multiprocessing import Process
import matplotlib.pyplot as plt
import histogram as htg
import aHash as ah
import pHash as ph
import dHash as dh
import sys
import os
import shutil

image_01_path=''
image_02_path=''
image_path=r'f:\\share'


def show_result(image_01_path, image_02_path, calMultipleHistogramSimilarity, calaHashSimilarity, calpHashSimilarity,
                caldHashSimilarity):
    # read image files
    img1 = Image.open(image_01_path)
    img2 = Image.open(image_02_path)

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
    print('依据图片直方图距离计算相似度：{}'.format(calMultipleHistogramSimilarity))

    # aHash Calculation
    print('依据平均哈希算法计算相似度：{}/{}'.format(calaHashSimilarity, 64))

    # pHash Calculation
    print('依据感知哈希算法计算相似度：{}/{}'.format(calpHashSimilarity, 64))

    # dHash Calculation
    print('依据差异哈希算法计算相似度：{}/{}'.format(caldHashSimilarity, 64))

    plt.rcParams['font.sans-serif'] = ['KaiTi']  # 指定默认字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

    plt.figure()
    plt.subplot(2, 2, 1)
    plt.imshow(img1)
    plt.title(os.path.split(image_01_path)[1])
    plt.xticks([])
    plt.yticks([])

    plt.subplot(2, 2, 3)
    plt.imshow(img2)
    plt.title(os.path.split(image_02_path)[1])
    plt.xticks([])
    plt.yticks([])

    plt.subplot(2, 2, 2)
    plt.plot(range(len(hg1)), hg1, color='blue', linewidth=1.5, label='img1')
    plt.plot(range(len(hg2)), hg2, color='red', linewidth=1.5, label='img2')
    plt.xticks([])
    plt.yticks([])

    string = '依据图片直方图距离计算相似度：\n{}'.format(calMultipleHistogramSimilarity)
    string += '\n\n'
    string += '依据平均哈希算法计算相似度：\n{}/{}'.format(calaHashSimilarity, 64)
    string += '\n\n'
    string += '依据感知哈希算法计算相似度：\n{}/{}'.format(calpHashSimilarity, 64)
    string += '\n\n'
    string += '依据差异哈希算法计算相似度：\n{}/{}'.format(caldHashSimilarity, 64)

    plt.subplot(2, 2, 4)
    plt.text(0.05, 0.05, string)
    plt.xticks([])
    plt.yticks([])

    plt.show()

def copy_file(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)
    shutil.copy(src, dst)

if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv)==2:
        if os.path.isdir(sys.argv[1]):
            image_path = os.path.abspath(sys.argv[1])
        else:
            print('not a dir')
    else:
        print('use default argv')

    print("image dir : %s"%image_path)

    images = os.listdir(image_path)

    image_index=0
    while image_index != len(images):
        if len(image_01_path)==0:
            image_01_path = os.path.join(image_path, images[image_index])
            image_index += 1
        if len(image_02_path)==0:
            image_02_path = os.path.join(image_path, images[image_index])
            image_index += 1

        img1 = Image.open(image_01_path)
        img2 = Image.open(image_02_path)
        # Histogram Similarity Calculation
        # regularize the images
        img1_htg = htg.regularizeImage(img1)
        img2_htg = htg.regularizeImage(img2)

        hg1 = img1_htg.histogram()
        # print(img1.histogram())
        # print('img1的样本点有{}个'.format(len(hg1)))
        hg2 = img2_htg.histogram()
        # print(img2.histogram())
        # print('img2的样本点有{}个'.format(len(hg2)))

        calMultipleHistogramSimilarity = htg.calMultipleHistogramSimilarity(img1_htg, img2_htg)
        calaHashSimilarity = ah.calaHashSimilarity(img1, img2)
        calpHashSimilarity = ph.calpHashSimilarity(img1, img2)
        caldHashSimilarity = dh.caldHashSimilarity(img1, img2)

        if (calMultipleHistogramSimilarity<0.5) or (calaHashSimilarity<50) or (calpHashSimilarity<50) or (caldHashSimilarity<50):
            print('image similar, %s, %s'%(image_01_path, image_02_path))
            # show_result(image_01_path, image_02_path, calMultipleHistogramSimilarity,
            #             calaHashSimilarity, calpHashSimilarity, caldHashSimilarity)
            shutil.copy(image_02_path, image_02_path+'-strip')
            copy_file(image_02_path, os.path.join(image_path, 'strip'))
            image_01_path = image_02_path
        else:
            print('no')

        image_02_path = os.path.join(image_path, images[image_index])
        image_index += 1

