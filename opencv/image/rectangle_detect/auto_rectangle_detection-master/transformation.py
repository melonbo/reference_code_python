#!/usr/bin/python
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('88.jpg')
rows,cols,ch = img.shape

pts1 = np.float32([[652,380],[2652,1144],[404,996],[2400,1796]])
pts2 = np.float32([[0,0],[1300,0],[0,300],[1300,300]])

M = cv2.getPerspectiveTransform(pts1,pts2)

dst = cv2.warpPerspective(img,M,(1300,300))
cv2.imwrite('transformation.png',dst)
plt.subplot(121),plt.imshow(img),plt.title('Input')
plt.subplot(122),plt.imshow(dst),plt.title('Output')
plt.show()
