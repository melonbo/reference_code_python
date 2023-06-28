import gc
import cv2
import random
import numpy as np
import sys
 
from PIL import ImageFile
from PIL import Image, ImageFont, ImageDraw, ImageFilter, ImageEnhance
from imgaug import augmenters as iaa
from sklearn.preprocessing import normalize as sknormalize
import multiprocessing
from math import pi
 
def pil_pad_image(img, rate,c=4):
    _h,_w = img.height, img.width
    w = rate*_w
    h = rate*_h
    mode = {3:"RGB", 4:"RGBA"}[c]
    new_img = Image.new(mode, (w,h))
    y = int((h - _h)/2)
    x = int((w - _w)/2)
    new_img.paste(img, ((x,y)))
    return new_img
 
def shrink(img):
    if not isinstance(img, np.ndarray):
        img = np.array(img)
    mask = img>0
    coords = np.argwhere(mask)
    if len(img.shape)==3:
        y0,x0,_ = coords.min(axis = 0)
        y1,x1,_ = coords.max(axis = 0)+1
        new_img = img[y0:y1,x0:x1,:]
    else:
        y0,x0 = coords.min(axis = 0)
        y1,x1 = coords.max(axis = 0)+1
        new_img = img[y0:y1,x0:x1]
    return Image.fromarray(np.uint8(new_img))
