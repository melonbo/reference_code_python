import matplotlib.pyplot as plt
from PIL import Image
import random
import os
# image_path = "/home/xsr-ai/datasets/butterfly.jpg"
from PIL import Image, ImageEnhance, ImageOps, ImageFile
import numpy as np
import random
import threading, os, time
import logging
 
logger = logging.getLogger(__name__)
ImageFile.LOAD_TRUNCATED_IMAGES = True
 
 
class DataAugmentation:
    """
    包含数据增强的八种方式
    """
 
 
    def __init__(self):
        pass
 
    @staticmethod
    def openImage(image):
        return Image.open(image, mode="r")
 
    @staticmethod
    def randomRotation(image, mode=Image.BICUBIC):
        """
         对图像进行随机任意角度(0~360度)旋转
        :param mode 邻近插值,双线性插值,双三次B样条插值(default)
        :param image PIL的图像image
        :return: 旋转转之后的图像
        """
        random_angle = np.random.randint(1, 5)
        return image.rotate(random_angle, mode)
 
    @staticmethod
    def randomCrop(image):
        """
        对图像随意剪切,考虑到图像大小范围(68,68),使用一个一个大于(36*36)的窗口进行截图
        :param image: PIL的图像image
        :return: 剪切之后的图像
        """
        image_width = image.size[0]
        image_height = image.size[1]
 
        crop_width = int(image_width*0.81649658092)
        crop_height = int(image_height*0.81649658092)
 
        # crop_win_size = np.random.randint(40, 68)
        random_region = (
            (image_width - crop_width) >> 1, (image_height - crop_height) >> 1, (image_width + crop_width) >> 1,
            (image_height + crop_height) >> 1)
        return image.crop(random_region)
 
    @staticmethod
    def randomColor(image):
        """
        对图像进行颜色抖动
        :param image: PIL的图像image
        :return: 有颜色色差的图像image
        """
        # random_factor = np.random.randint(8, 12) / 10.  # 随机因子
        # color_image = ImageEnhance.Color(image).enhance(random_factor)  # 调整图像的饱和度
        # random_factor = np.random.randint(8, 12) / 10.  # 随机因子
        # brightness_image = ImageEnhance.Brightness(color_image).enhance(random_factor)  # 调整图像的亮度
        # random_factor = np.random.randint(8, 15) / 10.  # 随机因1子
        # contrast_image = ImageEnhance.Contrast(brightness_image).enhance(random_factor)  # 调整图像对比度
        # random_factor = np.random.randint(8, 12) / 10.  # 随机因子
 
        random_factor = np.random.randint(5, 15) / 10.  # 随机因子
        color_image = ImageEnhance.Color(image).enhance(random_factor)  # 调整图像的饱和度
        random_factor = np.random.randint(8, 13) / 10.  # 随机因子
        brightness_image = ImageEnhance.Brightness(color_image).enhance(random_factor)  # 调整图像的亮度
        random_factor = np.random.randint(7, 17) / 10.  # 随机因1子
        contrast_image = ImageEnhance.Contrast(brightness_image).enhance(random_factor)  # 调整图像对比度
        random_factor = np.random.randint(5, 16) / 10.  # 随机因子
 
 
        return ImageEnhance.Sharpness(contrast_image).enhance(random_factor)  # 调整图像锐度
 
    @staticmethod
    def randomGaussian(image, mean=0.2, sigma=0.3):
        """
         对图像进行高斯噪声处理
        :param image:
        :return:
        """
 
        def gaussianNoisy(im, mean=0.2, sigma=0.3):
            """
            对图像做高斯噪音处理
            :param im: 单通道图像
            :param mean: 偏移量
            :param sigma: 标准差
            :return:
            """
            for _i in range(len(im)):
                im[_i] += random.gauss(mean, sigma)
            return im
 
        # 将图像转化成数组
        img = np.asarray(image)
        img.flags.writeable = True  # 将数组改为读写模式
        width, height = img.shape[:2]
        img_r = gaussianNoisy(img[:, :, 0].flatten(), mean, sigma)
        img_g = gaussianNoisy(img[:, :, 1].flatten(), mean, sigma)
        img_b = gaussianNoisy(img[:, :, 2].flatten(), mean, sigma)
        img[:, :, 0] = img_r.reshape([width, height])
        img[:, :, 1] = img_g.reshape([width, height])
        img[:, :, 2] = img_b.reshape([width, height])
        return Image.fromarray(np.uint8(img))
 
    @staticmethod
    def saveImage(image, path):
        image.save(path)
 
 
def imageOps(func_name, image, des_path, file_name, times=1):
    funcMap = {"randomRotation": DataAugmentation.randomRotation,
               "randomCrop": DataAugmentation.randomCrop,
               "randomColor": DataAugmentation.randomColor,
               "randomGaussian": DataAugmentation.randomGaussian
               }
    if funcMap.get(func_name) is None:
        logger.error("%s is not exist", func_name)
        return -1
 
    for _i in range(0, times, 1):
        new_image = funcMap[func_name](image)
        DataAugmentation.saveImage(new_image, os.path.join(des_path, func_name + str(_i) + file_name))
 
 
# opsList = {"randomRotation", "randomCrop", "randomColor", "randomGaussian"}
opsList = {"randomColor", "randomRotation"}
 
 
def threadOPS(image, crop_img_name):
 
    threadImage = [0] * 2
    _index = 0
 
    for ops_name in opsList:
        threadImage[_index] = threading.Thread(target=imageOps,
                                               args=(ops_name, image, save_path, crop_img_name))
        threadImage[_index].start()
        _index += 1
        time.sleep(0.2)
 
curPath = os.path.abspath('.')
 
 
 
def random_crop(image, crop_shape, padding=None):
    oshape = image.size
 
    if padding:
        oshape_pad = (oshape[0] + 2 * padding, oshape[1] + 2 * padding)
        img_pad = Image.new("RGB", (oshape_pad[0], oshape_pad[1]))
        img_pad.paste(image, (padding, padding))
 
        nh = random.randint(0, oshape_pad[0] - crop_shape[0])
        nw = random.randint(0, oshape_pad[1] - crop_shape[1])
        image_crop = img_pad.crop((nh, nw, nh + crop_shape[0], nw + crop_shape[1]))
 
        return image_crop
    else:
        print("WARNING!!! nothing to do!!!")
        return image
 
 
if __name__ == "__main__":
 
 
    # for bgname in ["fm", "ny"]:
    for bgname in ["fm"]:
 
        # for prename in ['yinshua_da', 'dianzi', 'yinshua_xiao', "shouxie"]:
        for prename in ["yinshua_da_shai"]:
            #
            # file_dir = "/media/crx/4f5a4954-cbbd-46a9-9c48-aeb156476154/netease/file/1program/3ad/0banzheng/pachongpic/google/0nologo_v6_all_" + bgname + "/"
            file_dir = "/media/crx/4f5a4954-cbbd-46a9-9c48-aeb156476154/netease/file/1program/3ad/0banzheng/17173_inference/17173_ny_dianzi_692_2of3/"
            # file_dir = os.path.join(curPath, bgname + "_" + prename)
            # save_path = "/media/crx/4f5a4954-cbbd-46a9-9c48-aeb156476154/netease/file/1program/3ad/0banzheng/pachongpic/google/0nologo_v7_all_" + bgname + "_aug/"
            save_path = "/media/crx/4f5a4954-cbbd-46a9-9c48-aeb156476154/netease/file/1program/3ad/0banzheng/17173_inference/17173_ny_dianzi_692_2of3_aug4/"
            # save_path = os.path.join(curPath, bgname + "_" + prename + "_aug")
 
            if not os.path.exists(save_path):
                # os.mkdir(save_path)
                os.makedirs(save_path)
 
 
            for img_name in os.listdir(file_dir):
                img_path = os.path.join(curPath, file_dir, img_name)
 
                image_src = Image.open(img_path)
                # crop_width = image_src.size[0] - 24
                # crop_height = image_src.size[1] - 24
 
 
 
                # crop_width = int(image_src.size[0]*0.81649658092)
                # crop_height = int(image_src.size[1]*0.81649658092)
                if image_src.size[0] < 200 and image_src.size[1] < 200:
                    print(img_name, " is too small")
                    continue
                else:
 
                    for i in range(2):
 
                        r = random.random()
 
                        if r <= 0.5:
                            image_src = image_src.transpose(Image.FLIP_LEFT_RIGHT)
                            if r <= 0.25:
                                image_src = image_src.transpose(Image.FLIP_TOP_BOTTOM)
                        if r > 0.5:
                            image_src = image_src.transpose(Image.ROTATE_90)
                            if r < 0.75:
                                image_src = image_src.transpose(Image.ROTATE_180)
                        # image_src = im.transpose(image_src.ROTATE_270)
 
                        crop_width = random.randint(int(image_src.size[0]*0.81649658092), int(image_src.size[0]*1))
                        crop_height = random.randint(int(image_src.size[1]*0.81649658092), int(image_src.size[1]*1))
 
 
                        image_dst_crop = random_crop(image_src, [crop_width, crop_height], padding=10)
 
                        # im = img_name.split('/')[-1][:-4]
 
                        # crop_img_path = os.path.join(curPath, save_path, "crop" + str(i+1) + img_name)
                        crop_img_path = os.path.join(curPath, save_path, img_name.split('/')[-1][:-5] + "_crop" + str(i+1) + ".jpg")
                        crop_img_name = img_name.split('/')[-1][:-4] + "_crop" + str(i+1) + ".jpg"
                        # image_dst_crop.save(crop_img_path)
 
                        # print("here!")
                        # threadOPS(image_dst_crop, crop_img_name)
                        threadOPS(image_dst_crop, crop_img_name)
 
