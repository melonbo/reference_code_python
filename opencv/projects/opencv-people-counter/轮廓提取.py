# import numpy as np
# import cv2
# import os
#
# im = cv2.imread('test.jpg')
# imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
# ret,thresh = cv2.threshold(imgray,127,255,0)
# image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#
# for i in range(0,len(contours)):
#   x, y, w, h = cv2.boundingRect(contours[i])
#   cv2.rectangle(image, (x,y), (x+w,y+h), (153,153,0), 5)
#
# newimage=image[y+2:y+h-2,x+2:x+w-2] # 先用y确定高，再用x确定宽
# nrootdir=("./")
#
# cv2.imwrite( nrootdir+str(i)+".jpg",newimage)
# print (i)


import cv2

# 读入图片
img = cv2.imread("test.jpg")

# 必须先转化成灰度图
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 二值化
ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# 寻找轮廓
thresh, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 画出轮廓，-1,表示所有轮廓，画笔颜色为(0, 255, 0)，即Green，粗细为3
cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

# 显示图片
cv2.namedWindow("Contours")
cv2.imshow("Contours", thresh)

# 等待键盘输入
cv2.waitKey(0)
cv2.destroyAllWindows()