import cv2
import numpy as np

# 读取图像
img = cv2.imread(r'F:\share\video\qd3\QD3-003-01-20220516-210000.mp4_002904.033.jpg')

# 创建SIFT对象
sift = cv2.xfeatures2d.SIFT_create()

# 检测关键点和描述符
kp, des = sift.detectAndCompute(img, None)

#定义个一个多边形
polygon = np.array([(200, 100), (500, 100), (500, 300), (200, 300)])

kp2 = []
for k in kp:
    if cv2.pointPolygonTest(polygon, k.pt, True)>0:
        kp2.append(k)
        # print(k)
print(type(kp2))
print(len(kp2))
# 可视化关键点
img_kp = cv2.drawKeypoints(img, kp2, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

cv2.polylines(img_kp, [polygon], isClosed=True, color=(0, 0, 255), thickness=3)
# 显示结果
cv2.imshow('keypoints', img_kp)
cv2.waitKey(0)
cv2.destroyAllWindows()