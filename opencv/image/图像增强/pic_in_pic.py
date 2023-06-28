# coding:utf-8
from __future__ import print_function, absolute_import
import threading
import os
import gc
import cv2
import random
import numpy as np
#imutilsimport
import sys
 
from PIL import ImageFile
from PIL import Image, ImageFont, ImageDraw, ImageFilter, ImageEnhance
from imgaug import augmenters as iaa
from sklearn.preprocessing import normalize as sknormalize
import multiprocessing
from math import pi
from utils import pil_pad_image, shrink
from copy import deepcopy
 
 
 
 
 
class BaseAugmenter(object):
    def __init__(self):
        pass 
    def augment_image(self,img):
        pass
    def augment_images(self,imgs):
        return [self.augment_image(img) for img in imgs ]
 
 
class RandomResize(BaseAugmenter):
    '''
    当scale是一个float
    当scale长度为2，则为最大值和最小值，在其中随机生成。
    当scale长度大于2，则为指定的几个值，在其中随机选
    当fix_pos = True时，按照示例图中的样子: 直接pad时，缩放后的图在黑边的最下边中央位置
    '''
    def __init__(self, scale=(0.5,0.9),keep_size=False,pad=True,fix_pos=True):
        self.scale = scale
        self.keep_size = False 
        self.pad = pad
        self.fix_pos = fix_pos
    def augment_image(self,img):
        _w, _h = img.width, img.height
        if isinstance(self.scale, float):
            h = int(self.scale*_h)
            w = int(self.scale*_w)
            new_img = img.resize((w,h))
        elif not self.keep_size:
            if len(self.scale) == 2:
                h = int(random.uniform(self.scale[0],self.scale[1])*_h)
                w = int(random.uniform(self.scale[0],self.scale[1])*_w)
            elif len(self.scale) > 2:
                h = int(random.choice(self.scale)*_h)
                w = int(random.choice(self.scale)*_w)
            new_img = img.resize((w,h))
        else:
            if len(self.scale) == 2:
                ratio = random.uniform(self.scale[0], self.scale[1])
            elif len(self.scale) >2:
                ratio = random.choice(self.scale)
            h,w = int(ratio*_h), int(ratio*_w)
            new_img = img.resize((w,h))
        
        if self.pad:
            bg = Image.new(new_img.mode, (_w, _h))
            if not self.fix_pos:
                x = random.randint(0, bg.width - new_img.width)
                y = random.randint(0, bg.height - new_img.height) 
                bg.paste(new_img, (x,y))
            else:
                x = int((bg.width-new_img.width)/2)
                y = bg.height - new_img.height
                bg.paste(new_img, (x,y))
            new_img = bg
        return new_img
 
 
class PicInPic(BaseAugmenter): 
    def __init__(self,bgimg_list_fname,keep_size,thresh1,thresh2,angle_r,angle_s):
        self.keep_size = keep_size
        self.thresh1 = thresh1
        self.thresh2 = thresh2
        self.angle = angle_r
        self.shear = iaa.Affine(shear=angle_s)
        self.bg_list = open(bgimg_list_fname).read().splitlines()
#        self.affine = iaa.Affine(
#            scale={"x": (0.8, 1.2), "y": (0.8, 1.2)}, # scale images to 80-120% of their size, individually per axis
#            translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)}, # translate by -20 to +20 percent (per axis)
#            rotate=(-45, 45), # rotate by -45 to +45 degrees
#            shear=(-30, 30), # shear by -16 to +16 degrees
#            order=[0, 1], # use nearest neighbour or bilinear interpolation (fast)
#            cval=(0, 255), # if mode is constant, use a cval between 0 and 255
#            mode=ia.ALL # use any of scikit-image's warping modes (see 2nd image from the top for examples)
#        )
 
    def affine(self, img):
        if img.mode == "RGB":
            new_img = img.convert("RGBA")
        elif img.mode == "P":
            new_img = img.convert("RGBA")
        else:
            # print(">>>>>>>>>>>>>", img.mode)
            new_img = img.convert("RGBA")
        new_img = pil_pad_image(new_img,3,4)
        if random.random() > self.thresh1:
            angle = random.uniform(self.angle[0], self.angle[1])
            new_img = new_img.rotate(angle)
            if random.random() > self.thresh2:
                new_img = Image.fromarray(self.shear.augment_image(np.array(new_img)))
        elif random.random() > self.thresh1:
            new_img = Image.fromarray(self.shear.augment_image(np.array(new_img)))
        new_img = shrink(new_img)
        return new_img
 
    def augment_image(self,img):
        bg_name = random.choice(self.bg_list)
        bg = Image.open(bg_name)
 
        r_wh = bg.width / bg.height
 
        while r_wh < 0.4 or r_wh > 2.5:
            print(bg_name, " r_wh yichang")
            # bg.show()
            bg_name = random.choice(self.bg_list)
            bg = Image.open(bg_name)
            r_wh = bg.width / bg.height
 
        bg = bg.convert("RGBA")
        # bg.show()
        # img.show()
        if self.keep_size:
            bg = bg.resize((img.width,img.height))
        new_img = self.affine(img)
 
        # new_img.show()
        ratio = min(float(bg.height)/new_img.height, float(bg.width)/new_img.width)
        # r = random.uniform(0.65*ratio, 0.9*ratio)
        r = random.uniform(0.7*ratio, 0.95*ratio)
        w,h = int(r*new_img.width), int(r*new_img.height)
        new_img = new_img.resize((w,h))
        r,g,b,a = new_img.split()
 
        mode_x = random.randint(0, 1)
        mode_y = random.randint(0, 1)
 
        if mode_x == 0:
            x = random.randint(0, int(0.25*(bg.width - new_img.width)))
        elif mode_x == 1:
            x = random.randint(int(0.75*(bg.width - new_img.width)), bg.width - new_img.width)
 
 
        if mode_y == 0:
            y = random.randint(0, int(0.25*(bg.height - new_img.height)))
        elif mode_y == 1:
            y = random.randint(int(0.75*(bg.height - new_img.height)), bg.height - new_img.height)
 
 
 
 
        # x = random.randint(0, bg.width - new_img.width)
        # y = random.randint(0, bg.height - new_img.height)
        # bgr = bg.paste(new_img,(x,y),mask=r)
        # bgr.show()
        # bgg = bg.paste(new_img,(x,y),mask=g)
        # bgg.show()
        # bgb = bg.paste(new_img,(x,y),mask=b)
        # bgb.show()
        # bga = bg.paste(new_img,(x,y),mask=a)
        # bga.show()
        bg.paste(new_img,(x,y),mask=a)
        # bg.show()
        # bg.show()
        return bg, bg_name
 
class Watermark(BaseAugmenter):
    def __init__(self, logolist_fname):
        self.logo_files = open(logolist_fname).read().splitlines()
    def augment_image(self, img):
        logo = Image.open(random.choice(self.logo_files))
        logo = logo.convert("RGBA")
        assert logo.mode == "RGBA"
        logo = pil_pad_image(logo,3,4)
        logo = logo.rotate(random.uniform(-180,180))
        logo = shrink(logo)
 
        ratio = min(float(img.height)/logo.height,  float(img.width)/logo.width)
        ratio = random.uniform(0.4,0.8)*ratio
        h,w = int(ratio*logo.height), int(ratio*logo.width)
        logo = logo.resize((w,h))
        x = random.randint(0, img.width - logo.width)
        y = random.randint(0, img.height - logo.height)
 
        r,g,b,a = logo.split()
        img.paste(logo, (x,y), mask=a)
        return img
 
class Mosaic(BaseAugmenter):
    def augment_image(self, img):
        if isinstance(img, Image.Image):
            img = np.array(img)
        img_height,img_width = img.shape[:2]
        random_x = random.uniform(0.3, 0.6)
        random_y = random.uniform(0.3, 0.6)
        masaic_width = int(img_width*random_x)
        masaic_height = int(img_height*random_y)
        paste_coordx = random.randint(0, img_width - masaic_width)
        paste_coordy = random.randint(0, img_height - masaic_height)
        size = random.randint(10,25)
        width_bin = int(masaic_width/float(size))
        height_bin = int(masaic_height/float(size))
        for x in range(width_bin):
            for y in range(height_bin):
                img[paste_coordy+y*size:paste_coordy+(y+1)*size,paste_coordx+x*size:paste_coordx+(x+1)*size,:] = img[paste_coordy+y*size,paste_coordx+x*size,:]
        return Image.fromarray(img)
 
class SaltNoise(BaseAugmenter):
    def __init__(self, p):
        self.func = iaa.SaltAndPepper(p=p)
    def augment_image(self,img):
        if isinstance(img, Image.Image):
            img = np.array(img)
        img = self.func.augment_image(img)
        return Image.fromarray(img)
 
class WhiteNoise(BaseAugmenter):
    def __init__(self,loc,scale,per_channel):
        self.func = iaa.AdditiveGaussianNoise(loc=loc,scale=scale,per_channel=per_channel)
    def augment_image(self,img):
        if isinstance(img, Image.Image):
            img = np.array(img)
        img = self.func.augment_image(img)
        return Image.fromarray(img)
 
class ColorToGray(BaseAugmenter):
    def __init__(self):
        if random.random()>0.1:
            self.func = iaa.Sequential([
            iaa.Grayscale(alpha=(0.1,1.0)),
            iaa.ContrastNormalization((0.5, 2.0), per_channel=0.5),
            iaa.Add(value=(-45,45))
            ],
            random_order=False)
        else:
            self.func = iaa.Sequential([
            iaa.Grayscale(alpha=(0.5,1.0)),
            ],
            random_order=False)
    def augment_image(self,img):
        if isinstance(img, Image.Image):
            img = np.array(img)
        img = self.func.augment_image(img)
        return Image.fromarray(img)
 
 
 
def all_augment(img, k):
    results = []
    # for func, name in zip([pic_in_pic,mosaic,color_to_gray,watermark], ["picInPic","mosaic","gray","watermark"]):
    for func, name in zip([pic_in_pic,mosaic,color_to_gray,watermark], ["picInPic"]):
        for i in range(k):
            #
            # if image_src.size[0] < 200 and image_src.size[1] < 200:
            #     print(img_name, " is too small")
            #     continue
 
 
 
            # res_img = random_resize.augment_image(deepcopy(img))
            res_img, bg_name = func.augment_image(deepcopy(img))
            results.append((name + '_' + str(i), res_img, bg_name))
    # for func, name in zip([white_noise, salt_noise], ["white_noise","salt_noise"]):
    #     for i in range(5):
    #         res_img = func.augment_image(deepcopy(img))
    #         results.append((name + '_' + str(i), res_img))
    # for i in range(10):
    #     res_img = random_resize.augment_image(deepcopy(img))
    #     if i % 2 == 0:
    #         res_img = res_img.transpose(Image.FLIP_LEFT_RIGHT)
    #     else:
    #         res_img = res_img.transpose(Image.FLIP_TOP_BOTTOM)
    #     results.append(("random_resize_" + str(i),res_img))
 
    return results
 
 
# for bg_fix in ["fengmian", "neiye"]:
for bg_fix in ["fengmian", "neiye"]:
    BG_LIST_FILE = "bg_v6_" + bg_fix + "_aug.txt"
 
 
    # BG_LIST_FILE = "bg_v6_fengmian_aug.txt"
    # LOGO_LIST_FILE = "logo_v6_kuang_dianzi.txt"
    # LOGO_LIST_FILE = "logo_v6_kuang_shengcheng_text.txt"
    # LOGO_LIST_FILE = "logo_v6_kuang_shouxie_rectango.txt"
 
    # for LOGO_fix in ["dianzi", "shouxie_square", "logo_v6_kuang_shouxie_rectango_xi", "shengcheng_text", "yinshua" ]:
    for LOGO_fix in ["shengcheng_text"]:
 
 
        LOGO_LIST_FILE = "logo_v6_kuang_" + LOGO_fix + ".txt"
        # LOGO_LIST_FILE = "logo_v6_kuang_yinshua.txt"
 
        # IMG_LIST_FILE = "/home/netease/code/homologous_image_retrieval/data/imgs.txt"
 
        if bg_fix == "fengmian":
            if LOGO_fix == "dianzi": k = 26
            elif LOGO_fix == "shouxie_square": k = 59
            elif LOGO_fix == "shouxie_rectango": k = 48
            elif LOGO_fix == "shengcheng_text": k = 22
            elif LOGO_fix == "yinshua": k = 20
            elif LOGO_fix == "shouxie_rectango_xi": k = 30
            elif LOGO_fix == "shouxie_rectango_cu": k = 30
 
        if bg_fix == "neiye":
            if LOGO_fix == "dianzi": k = 12
            elif LOGO_fix == "shouxie_square": k = 36
            elif LOGO_fix == "shouxie_rectango": k = 30
            elif LOGO_fix == "shengcheng_text": k = 8
            elif LOGO_fix == "yinshua": k = 10
            elif LOGO_fix == "shouxie_rectango_xi": k = 30
            elif LOGO_fix == "shouxie_rectango_cu": k = 30
 
 
        k = 15
 
 
 
 
        IMG_LIST_FILE = LOGO_LIST_FILE
 
        salt_noise = SaltNoise(p=(0.05, 0.25))
        white_noise = WhiteNoise(loc=0, scale=(0.05 * 255, 0.20 * 255), per_channel=0.5)
        pic_in_pic = PicInPic(bgimg_list_fname=BG_LIST_FILE, keep_size=False, thresh1=0.5, thresh2=0.5, angle_r=(-70, 70),
                              angle_s=(-0, 0))
        random_resize = RandomResize(scale=[0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.9])
        mosaic = Mosaic()
        color_to_gray = ColorToGray()
 
        watermark = Watermark(LOGO_LIST_FILE)
 
        i=0
        curPath = os.path.abspath('.')
 
        for imgname in open(IMG_LIST_FILE).read().splitlines():
            img = Image.open(imgname)
            print(imgname)
 
 
 
 
            results = all_augment(img, k)
            # save_path = "5output_goodlogo_v2/"+str(i)+'/'
            save_path = "5output_goodlogo_v10_new/" + bg_fix + "_kuang_" + LOGO_fix + "_07to095_shear0_" + str(k) + "/"
            save_path = os.path.join(curPath, save_path)
 
            # print(os.path.exists(save_path))
 
            if not os.path.exists(save_path):
                # os.mkdir(save_path)
                os.makedirs(save_path)
            for name, res_img, bg_name in results:
                # res_name = save_path + imgname.split('/')[-1][:-4] + '_' + name + '.png'
                res_name = save_path + imgname.split('/')[-1][:-4] + '_' + bg_name.split('/')[-1][:-4] + '.png'
                res_img.save(res_name)
            i+=1
 
