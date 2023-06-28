# python color_kmeans.py --image images/cactus.jpg --clusters 3
# 导入必要的包
import argparse
import cv2
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans


def centroid_histogram(clt):
    # 获取不同聚簇的个数，根据每个聚簇的像素数生成直方图
    # k均值算法将图像中的每个像素分配给最近的聚类。
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)
    # 对直方图进行归一化，使得总和为1
    hist = hist.astype("float")
    hist /= hist.sum()
    # 返回直方图
    return hist


# plot_colors函数需要两个参数：
# hist，它是从centroid_histogram函数生成的直方图；
# centroids，是由k-means算法生成的质心（集群中心）的列表。
def plot_colors(hist, centroids):
    # 初始化代表相对频率的每种颜色的条形图
    # 定义了一个300×50像素的矩形，以容纳图像中最主要的颜色
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0
    # 遍历每一个聚簇的百分比及颜色
    for (percent, color) in zip(hist, centroids):
        # 绘制每一聚簇的相对百分比
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX
    # 返回条形图
    return bar
# 构建命令行参数和解析
# --image 原始图像路径
# --clusters 期望生成的簇数
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
ap.add_argument("-c", "--clusters", required=True, type=int,
                help="# of clusters")
args = vars(ap.parse_args())
# 加载图像，转换BGR-->RGB 以在matplotlib展示
image = cv2.imread(args["image"])
# image = cv2.imread(r"F:\share\video\qd3\QD3-003-01-20220516-210000.mp4_002904.033.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# 展示图像
plt.figure()
plt.axis("off")
plt.imshow(image)
# 将NumPy数组重塑为RGB像素列表
image = image.reshape((image.shape[0] * image.shape[1], 3))
# 使用scikit-learn中的K-means实现来避免重新实现该算法
# 使用K-means查找图像中最主要的颜色
# 使用期望获取的聚簇数，初始化局KMeans类，调用fit()方法将像素列表聚集在一起
clt = KMeans(n_clusters=args["clusters"])
clt.fit(image)
# 构建聚簇直方图
# 建立图表以代表每一种颜色所对应的像素数
print(clt)

# hist = utils.centroid_histogram(clt)
# bar = utils.plot_colors(hist, clt.cluster_centers_)
# 展示颜色条形图
# plt.figure()
# plt.axis("off")
# plt.imshow(bar)
# plt.show()
