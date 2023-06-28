import matplotlib
import matplotlib.pyplot as plt
import cv2 as cv
image = cv.imread(r"F:\share\video\qd3\QD3-003-01-20220516-210000.mp4_002904.033.jpg")

# 读入彩色图像
hist1 = cv.calcHist([image],[0],None,[256],[0,255])
# 计算直方图数据（蓝色）
hist2 = cv.calcHist([image],[1],None,[256],[0,255])
# 计算直方图数据（绿色）
hist3 = cv.calcHist([image],[2],None,[256],[0,255])
# 计算直方图数据（红色）
plt.plot(hist1)
# 绘制直方图
plt.plot(hist2)
# 绘制直方图
plt.plot(hist3)
# 绘制直方图
plt.show()