import cv2
import numpy as np

# 定义一个多边形
polygon = np.array([[0, 0], [10, 0], [10, 10], [0, 10]])

# 测试一个点，不计算距离
point = (5, 5)
result = cv2.pointPolygonTest(polygon, point, False)

# 打印结果
print(result)