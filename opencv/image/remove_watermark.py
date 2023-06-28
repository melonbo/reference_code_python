#coding=utf-8

import cv2
import numpy as np

path=r"F:\share\123456789.jpg"

def deal_image(path):
    img0 = cv2.imread(path)
    hight, width, depth = img0.shape[0:3]
    #图片二值化处理，把[240, 240, 240]~[255, 255, 255]以外的颜色变成0
    thresh = cv2.inRange(img0, np.array([240, 240, 240]), np.array([255, 255, 255]))
    #创建形状和尺寸的结构元素
    kernel = np.ones((3, 3), np.uint8)
    #扩张待修复区域
    hi_mask = cv2.dilate(thresh, kernel, iterations=1)
    #插值
    img1 = cv2.inpaint(img0, hi_mask, 5, flags=cv2.INPAINT_TELEA)
    return img0, img1, width, hight

def show2image(img0, img1, width, hight):
    cv2.namedWindow("Image", 0)
    cv2.resizeWindow("Image", int(width / 2), int(hight / 2))
    cv2.imshow("Image", img0)
    cv2.namedWindow("newImage", 0)
    cv2.resizeWindow("newImage", int(width / 2), int(hight / 2))
    cv2.imshow("newImage", img1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

img0,img1,width,hight = deal_image(path)
show2image(img0,img1,width,hight)