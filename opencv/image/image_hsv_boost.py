import cv2
import numpy as np
import random
import math


def get_illum_mean_and_std(img):
    is_gray = img.ndim == 2 or img.shape[1] == 1
    if is_gray:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    illum = hsv[..., 2] / 255.
    return np.mean(illum), np.std(illum)

# HSV增强（参考：YOLOv5）
def augment_hsv(img, hgain=0.02, sgain=1.6, vgain=0.06):
    # r = np.random.uniform(-1, 1, 3) * [hgain, sgain, vgain] + 1  # random gains
    r = list(map(lambda x: x + 1, [hgain, sgain, vgain]))
    hue, sat, val = cv2.split(cv2.cvtColor(img, cv2.COLOR_BGR2HSV))
    dtype = img.dtype  # uint8

    x = np.arange(0, 256, dtype=np.int16)
    lut_hue = ((x * r[0]) % 180).astype(dtype)
    lut_sat = np.clip(x * r[1], 0, 255).astype(dtype)
    lut_val = np.clip(x * r[2], 0, 255).astype(dtype)

    img_hsv = cv2.merge((cv2.LUT(hue, lut_hue), cv2.LUT(sat, lut_sat), cv2.LUT(val, lut_val))).astype(dtype)
    cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR, dst=img)  # no return needed


# path = r"F:\share\video\qd3\xx\rail-car-day-00025.jpg"
path = r"F:\share\video\qd3\light-detect\rail-car-day\rail-car-day-00025.jpg"
img = cv2.imread(path)
img = cv2.resize(img, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)
print(img)
# b,g,r = cv2.split(img)
# cv2.imshow('b', b)
# cv2.imshow('g', g)
# cv2.imshow('r', r)

cv2.namedWindow('hsv')
cv2.createTrackbar('h', 'hsv', 0, 30, lambda x:x)
cv2.createTrackbar('s', 'hsv', 0, 30, lambda x:x)
cv2.createTrackbar('v', 'hsv', 0, 30, lambda x:x)
while True:
    img_copy = img.copy()
    print(id(img), id(img_copy))
    h = cv2.getTrackbarPos('h', 'hsv')
    s = cv2.getTrackbarPos('s', 'hsv')
    v = cv2.getTrackbarPos('v', 'hsv')
    augment_hsv(img_copy, h/10, s/10, v/10)
    cv2.imshow('hsv', img_copy)
    cv2.waitKey(100)

