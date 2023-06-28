import numpy as np
import cv2
from PIL import Image, ImageFilter


def pillow_crop(path, x1, y1, x2, y2):
    im_path = path
    im = Image.open(im_path)
    width, height = im.size
    cropedIm = im.crop((x1, y1, x2, y2))
    # cropedIm.show()
    return cropedIm
# pillow_crop(r'1.jpg', 70, 10, 120, 100).show()


def pillow_new(path, w, h, color):
    newIm = Image.new('RGB', (w, h), 'red')
    # newIm.save(path)
    return newIm
# pillow_new(r'3.jpg', 100, 100, 'red').show()


def pillow_resize(src, dst, w, h):
    im = Image.open(src)
    resizedIm = im.resize((w, h))
    resizedIm.save(dst)
    return resizedIm
# pillow_resize(r'1.jpg', r'3.jpg', 200, 200).show()


def pillow_rotate(src, dst, angle):
    im=Image.open(src)
    retateIm = Image.open(src)
    dst = retateIm.rotate(angle)
    return dst
# pillow_rotate(r'1.jpg', r'3.jpg', 45).show()

# 镜像
def pillow_transpose(src, dst, angle):
    im=Image.open(src)
    retateIm = Image.open(src)
    dst = retateIm.rotate(angle)
    return dst
# pillow_transpose(r'1.jpg', r'3.jpg', 45).show()

# # 高斯模糊
# im.filter(ImageFilter.GaussianBlur).save(r'C:\Users\Administrator\Desktop\GaussianBlur.jpg')
# # 普通模糊
# im.filter(ImageFilter.BLUR).save(r'C:\Users\Administrator\Desktop\BLUR.jpg')
# # 边缘增强
# im.filter(ImageFilter.EDGE_ENHANCE).save(r'C:\Users\Administrator\Desktop\EDGE_ENHANCE.jpg')
# # 找到边缘
# im.filter(ImageFilter.FIND_EDGES).save(r'C:\Users\Administrator\Desktop\FIND_EDGES.jpg')
# # 浮雕
# im.filter(ImageFilter.EMBOSS).save(r'C:\Users\Administrator\Desktop\EMBOSS.jpg')
# # 轮廓
# im.filter(ImageFilter.CONTOUR).save(r'C:\Users\Administrator\Desktop\CONTOUR.jpg')
# # 锐化
# im.filter(ImageFilter.SHARPEN).save(r'C:\Users\Administrator\Desktop\SHARPEN.jpg')
# # 平滑
# im.filter(ImageFilter.SMOOTH).save(r'C:\Users\Administrator\Desktop\SMOOTH.jpg')
# # 细节
# im.filter(ImageFilter.DETAIL).save(r'C:\Users\Administrator\Desktop\DETAIL.jpg')
def pillow_GaussianBlur(src):
    im = Image.open(src)
    return im.filter(ImageFilter.FIND_EDGES)
# pillow_GaussianBlur(r"1.jpg").show()

