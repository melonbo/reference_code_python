# https://blog.csdn.net/SkyeBeFreeman/article/details/77972174
# example python "E:\work\pycode\util\opencv\picture\identify-similar-images-master\getFrameFromVideo.py" QD3-035-01-20220609-072511.mp4 25
from PIL import Image
from multiprocessing import Process
import matplotlib.pyplot as plt
import histogram as htg
import aHash as ah
import pHash as ph
import dHash as dh
import sys
import os
import cv2
import numpy as np

# image_01=np.random.rand(720,1080,3)
# image_02=np.random.rand(720,1080,3)
image_01=''
image_02=''
image_path=r'f:\\share'
frame_num = 0
frame_freq = 100
frame_num_01 = 0
frame_num_02 = 0


video_name=''

if __name__ == '__main__':
    if len(sys.argv)==3:
        video_name = sys.argv[1]
        frame_freq = int(sys.argv[2])
    elif len(sys.argv)==2:
        video_name = sys.argv[1]
    else:
        print('use default argv')

    frame_num = 0

    video_capture = cv2.VideoCapture(os.path.abspath(video_name))
    image_save_path = os.path.abspath(video_name).split('.')[0]
    print(image_save_path)

    if os.path.isdir(image_save_path):
        print('dir exist')
    else:
        print('dir not exist')
        os.mkdir(image_save_path)

    while True:
        # is_successfully_read, im = video_capture.read()
        is_successfully_read = video_capture.grab()

        if not is_successfully_read:
            print('read frame error, exit')
            break

        if not image_01:
            is_successfully_read, im = video_capture.retrieve()
            image_01 = Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB))
            image_01_frame_index = frame_num
            frame_num += 1
            continue

        if not image_02:
            is_successfully_read, im = video_capture.retrieve()
            image_02 = Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB))
            image_02_frame_index = frame_num
            frame_num += 1
            continue

        if (frame_num-image_02_frame_index) != frame_freq:
            frame_num += 1
            continue

        is_successfully_read, im = video_capture.retrieve()
        image_02 = Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB))
        image_02_frame_index = frame_num
        frame_num += 1

        # regularize the images
        # img1_htg = htg.regularizeImage(image_01)
        # img2_htg = htg.regularizeImage(image_02)
        img1_htg = image_01.resize((256,256)).convert('RGB')
        img2_htg = image_02.resize((256,256)).convert('RGB')

        hg1 = img1_htg.histogram()
        hg2 = img2_htg.histogram()

        calMultipleHistogramSimilarity = htg.calMultipleHistogramSimilarity(img1_htg, img2_htg)
        calaHashSimilarity = ah.calaHashSimilarity(image_01, image_02)
        calpHashSimilarity = ph.calpHashSimilarity(image_01, image_02)
        caldHashSimilarity = dh.caldHashSimilarity(image_01, image_02)

        string = ''
        string = '依据图片直方图距离计算相似度：\n{}'.format(calMultipleHistogramSimilarity)
        string += '\n\n'
        string += '依据平均哈希算法计算相似度：\n{}/{}'.format(calaHashSimilarity, 64)
        string += '\n\n'
        string += '依据感知哈希算法计算相似度：\n{}/{}'.format(calpHashSimilarity, 64)
        string += '\n\n'
        string += '依据差异哈希算法计算相似度：\n{}/{}'.format(caldHashSimilarity, 64)

        if (calMultipleHistogramSimilarity<0.5) or (calaHashSimilarity<50) or (calpHashSimilarity<50) or (caldHashSimilarity<50):
            # print('image similar, %s, %s'%(image_01_path, image_02_path))
            print('unsimilar between frame % and %d, at frame_freq %d'%(image_01_frame_index, image_02_frame_index, frame_freq), flush=True)
            print(string)
            cv2.imwrite(os.path.join(image_save_path, video_name.split('.')[0] + '-' + '{:0>5d}'.format(frame_num) + '.jpg'), im)
            image_01 = image_02
            image_01_frame_index = image_02_frame_index
            if len(sys.argv)==2:
                frame_freq = 100
        else:
            print('similar between frame %d and %d, at frame_freq %d'%(image_01_frame_index, image_02_frame_index, frame_freq), flush=True)
            if len(sys.argv)==2:
                frame_freq += 100

