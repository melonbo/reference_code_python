import cv2
import time
import numpy as np

# 读取前一帧和后一帧图像
prev_frame = cv2.imread(r'F:\share\video\qd3\light-detect\rail-car-night\rail-car-night-06150.jpg', 0)
next_frame = cv2.imread(r'F:\share\video\qd3\light-detect\rail-car-night\rail-car-night-06200.jpg', 0)

x, y, w, h = 100, 100, 500, 500
roi_prev_frame = prev_frame[y:y+h, x:x+w]
roi_next_frame = next_frame[y:y+h, x:x+w]

# 创建SIFT对象
sift = cv2.xfeatures2d.SIFT_create()

# 提取特征点和特征描述子
a=time.time()
prev_kp, prev_desc = sift.detectAndCompute(roi_prev_frame, None)
next_kp, next_desc = sift.detectAndCompute(roi_next_frame, None)
b=time.time()
print("提取特征点和特征描述子%.2f"%(b-a))
a=time.time()


prev_kp_select, prev_desc_select = [], []
next_kp_select, next_desc_select = [], []

for i, k in enumerate(prev_kp):
    if k.response > 0.03:
        prev_kp_select.append(prev_kp[i])
        prev_desc_select.append(prev_desc[i])
print(len(prev_kp_select), len(prev_kp))

for i, k in enumerate(next_kp):
    if k.response > 0.03:
        next_kp_select.append(next_kp[i])
        next_desc_select.append(next_desc[i])
print(len(next_kp_select), len(next_kp))

prev_kp_select, prev_desc_select = tuple(prev_kp_select), np.array(prev_desc_select)
next_kp_select, next_desc_select = tuple(next_kp_select), np.array(next_desc_select)



prev_kp, prev_desc = prev_kp_select, prev_desc_select
next_kp, next_desc = next_kp_select, next_desc_select

# 创建FLANN匹配器
matcher = cv2.FlannBasedMatcher()

# 对前后两帧图像的特征点进行匹配
matches = matcher.match(prev_desc, next_desc)
b=time.time()
print("对前后两帧图像的特征点进行匹配%.2f"%(b-a))
a=time.time()
# 筛选匹配结果
good_matches = []
for match in matches:
    if match.distance < 0.5 * len(prev_kp):
        good_matches.append(match)
b=time.time()
print("筛选匹配结果%.2f"%(b-a))
a=time.time()
print(len(matches), len(good_matches))
# 获取相似特征点的相对位置
prev_pts = []
next_pts = []
distance_x = 0
distance_y = 0
for match in good_matches:
    prev_pts.append(prev_kp[match.queryIdx].pt)
    next_pts.append(next_kp[match.trainIdx].pt)
    distance_x = next_kp[match.trainIdx].pt[0]-prev_kp[match.queryIdx].pt[0]
    distance_y = next_kp[match.trainIdx].pt[1] - prev_kp[match.queryIdx].pt[1]
    # print(distance_x,distance_y, prev_kp[match.queryIdx].response, next_kp[match.queryIdx].response)
b=time.time()
print("获取相似特征点的相对位置%.2f"%(b-a))
a=time.time()
# 计算车辆转动方向和角度
# 此处省略，可以根据相似特征点的相对位置进行计算

# 显示匹配结果
result = cv2.drawMatches(roi_prev_frame, prev_kp, roi_next_frame, next_kp, good_matches, None)
cv2.imshow('result', result)
cv2.waitKey(0)

