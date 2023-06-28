import cv2
import numpy as np

# 读取图像并转为灰度图像
img = cv2.imread(r'F:\share\image\06eb9db729d99eec52112cd3365b6b1f_1440w.webp')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 二值化图像
ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# 寻找轮廓
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 选择一个轮廓
contour = contours[0]
print(np.shape(contour))
print('contour', contour)

# 定义一个测试点
test_point = (100, 100)
# 定义一个多边形
polygon = [(0, 0), (10, 0), (10, 10), (0, 10)]
# 计算测试点到轮廓的最短距离
distance = cv2.pointPolygonTest(contour, test_point, True)

# 判断测试点是否在轮廓内部
if distance > 0:
    print('Test point is inside the contour')
elif distance == 0:
    print('Test point is on the contour')
else:
    print('Test point is outside the contour')

# 在图像上绘制轮廓和测试点
cv2.drawContours(img, [contour], 0, (0, 0, 255), 2)
cv2.circle(img, test_point, 5, (0, 255, 0), -1)

# 显示结果
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
