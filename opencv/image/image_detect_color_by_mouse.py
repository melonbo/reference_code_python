import cv2
import torch
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import PIL
from sklearn.cluster import KMeans
from collections import Counter
import time

def show_img_compar(img_1, img_2 ):
    f, ax = plt.subplots(1, 2, figsize=(400,300), dpi=1)
    ax[0].imshow(img_1)
    ax[1].imshow(img_2)
    ax[0].axis('off')
    ax[1].axis('off')
    f.tight_layout()
    plt.show()

def palette(clusters):
    width=300
    palette = np.zeros((50, width, 3), np.uint8)
    steps = width/clusters.cluster_centers_.shape[0]
    for idx, centers in enumerate(clusters.cluster_centers_):
        palette[:, int(idx*steps):(int((idx+1)*steps)), :] = centers
    return palette


def palette_perc(k_cluster):
    width = 300
    palette = np.zeros((50, width, 3), np.uint8)

    n_pixels = len(k_cluster.labels_)
    counter = Counter(k_cluster.labels_)  # count how many pixels per cluster
    perc = {}
    for i in counter:
        perc[i] = np.round(counter[i] / n_pixels, 2)
    perc = dict(sorted(perc.items()))

    # for logging purposes
    # print(perc)
    # print(k_cluster.cluster_centers_)

    step = 0

    for idx, centers in enumerate(k_cluster.cluster_centers_):
        palette[:, step:int(step + perc[idx] * width + 1), :] = centers
        step += int(perc[idx] * width + 1)

    return palette

def color_cluster_priority(k_cluster):
    n_pixels = len(k_cluster.labels_)
    counter = Counter(k_cluster.labels_)  # count how many pixels per cluster
    perc = {}
    color = {'red': 0.0, 'green': 0.0, 'blue': 0.0, 'yellow': 0.0, 'white': 0.0, 'black': 0.0, 'gray': 0.0,
             'orange': 0.0, 'cyan': 0.0, 'purple': 0.0, 'unknown': 0.0}
    for i in counter:
        perc[i] = np.round(counter[i] / n_pixels, 2)
    perc = dict(sorted(perc.items()))

    for idx, centers in enumerate(k_cluster.cluster_centers_):
        hsv = rgb2hsv(centers[0], centers[1], centers[2])
        c = color_enum(hsv)
        color[c] = perc[idx]
        print(centers, c, color[c])

    if color['red'] > 0:
        return 'red'
    if color['green'] > 0:
        return 'green'
    if color['blue'] > 0:
        return 'blue'
    if color['yellow'] > 0:
        return 'yellow'
    if color['white'] > 0:
        return 'white'

    if color['gray'] > 0:
        return 'white'
    if color['orange'] > 0:
        return 'yellow'

    if color['cyan'] > 0:
        return 'green'

    if color['purple'] > 0:
        return 'purple'
    if color['black'] > 0:
        return 'black'
    if color['unknown'] > 0:
        return 'unknown'


hsv_red_min_01 = np.array([0, 20, 46])  # 红色阈值下界
hsv_red_max_01 = np.array([12, 255, 255])  # 红色阈值上界
hsv_red_min_02 = np.array([156, 20, 46])  # 红色阈值下界
hsv_red_max_02 = np.array([180, 255, 255])  # 红色阈值上界
hsv_green_min = np.array([35, 20, 46])  # 绿色阈值下界
hsv_green_max = np.array([77, 255, 255])  # 绿色阈值上界
hsv_yellow_min = np.array([26, 20, 46])  # 黄色阈值下界
hsv_yellow_max = np.array([34, 255, 255])  # 黄色阈值上界
hsv_blue_min = np.array([100, 20, 46])  # 蓝色阈值下界
hsv_blue_max = np.array([124, 255, 255])  # 蓝色阈值上界
hsv_white_min = np.array([0, 0, 221])  # 白色阈值下届
hsv_white_max = np.array([180, 20, 255])  # 白色阈值上届
hsv_black_min = np.array([0, 0, 0])  # 黑色阈值下届
hsv_black_max = np.array([180, 255, 46])  # 黑色阈值上届
hsv_gray_min = np.array([0, 0, 46])  # 灰色阈值下届
hsv_gray_max = np.array([180, 20, 220])  # 灰色阈值上届
hsv_orange_min = np.array([11, 20, 46])  # 橙色阈值下届
hsv_orange_max = np.array([25, 255, 255])  # 橙色阈值上届
hsv_cyan_min = np.array([78, 20, 46])  # 青色阈值下届
hsv_cyan_max = np.array([99, 255, 255])  # 青色阈值上届
hsv_purple_min = np.array([125, 20, 46])  # 紫色阈值下届
hsv_purple_max = np.array([155, 255, 255])  # 紫色阈值上届


def color_enum(hsv):
    if inRangeList(hsv, hsv_red_max_01, hsv_red_min_01):
        print('红色01')
        return 'red'
    if inRangeList(hsv, hsv_red_max_02, hsv_red_min_02):
        print('红色02')
        return 'red'
    if inRangeList(hsv, hsv_green_max, hsv_green_min):
        print('绿色')
        return 'green'
    if inRangeList(hsv, hsv_blue_max, hsv_blue_min):
        print('蓝色')
        return 'blue'
    if inRangeList(hsv, hsv_yellow_max, hsv_yellow_min):
        print('黄色')
        return 'yellow'
    if inRangeList(hsv, hsv_white_max, hsv_white_min):
        print('白色')
        return 'white'
    if inRangeList(hsv, hsv_black_max, hsv_black_min):
        print('黑色')
        return 'black'
    if inRangeList(hsv, hsv_gray_max, hsv_gray_min):
        print('灰色')
        return 'gray'
    if inRangeList(hsv, hsv_orange_max, hsv_orange_min):
        print('橙色')
        return 'orange'
    if inRangeList(hsv, hsv_cyan_max, hsv_cyan_min):
        print('青色')
        return 'cyan'
    if inRangeList(hsv, hsv_purple_max, hsv_purple_min):
        print('紫色')
        return 'purple'
    print('unknown color', hsv)
    return 'unknown'


def inRangeList(arr, up, low):
    size = len(arr)
    for i in range(size):
        if arr[i] > up[i]:
            return False
        if arr[i] < low[i]:
            return False
    return True


def rgb2hsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx - mn
    # print(r, g, b, mx, mn, df)
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g - b) / df) + 360) % 360
    elif mx == g:
        h = (60 * ((b - r) / df) + 120) % 360
    elif mx == b:
        h = (60 * ((r - g) / df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df / mx
    v = mx
    return h / 2, s * 255, v * 255


def square_edge_value(img):
    h = img.shape[0]
    w = img.shape[1]

    sb = img[0, :, 0].sum() + img[h - 1, :, 0].sum() + img[:, 0, 0].sum() + img[:, w - 1, 0].sum()
    sb = sb / (w + w + h + h + 4)
    sg = img[0, :, 1].sum() + img[h - 1, :, 1].sum() + img[:, 0, 1].sum() + img[:, w - 1, 1].sum()
    sg = sg / (w + w + h + h + 4)
    sr = img[0, :, 2].sum() + img[h - 1, :, 2].sum() + img[:, 0, 2].sum() + img[:, w - 1, 2].sum()
    sr = sr / (w + w + h + h + 4)
    return sb, sg, sr

def xyxy2xywh(x):
    # Convert nx4 boxes from [x1, y1, x2, y2] to [x, y, w, h] where xy1=top-left, xy2=bottom-right
    y = x.clone() if isinstance(x, torch.Tensor) else np.copy(x)
    y[:, 0] = (x[:, 0] + x[:, 2]) / 2  # x center
    y[:, 1] = (x[:, 1] + x[:, 3]) / 2  # y center
    y[:, 2] = x[:, 2] - x[:, 0]  # width
    y[:, 3] = x[:, 3] - x[:, 1]  # height
    return y

def xywh2xyxy(x):
    # Convert nx4 boxes from [x, y, w, h] to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
    y = x.clone() if isinstance(x, torch.Tensor) else np.copy(x)
    y[:, 0] = x[:, 0] - x[:, 2] / 2  # top left x
    y[:, 1] = x[:, 1] - x[:, 3] / 2  # top left y
    y[:, 2] = x[:, 0] + x[:, 2] / 2  # bottom right x
    y[:, 3] = x[:, 1] + x[:, 3] / 2  # bottom right y
    return y

def clip_coords(boxes, shape):
    # Clip bounding xyxy bounding boxes to image shape (height, width)
    if isinstance(boxes, torch.Tensor):  # faster individually
        boxes[:, 0].clamp_(0, shape[1])  # x1
        boxes[:, 1].clamp_(0, shape[0])  # y1
        boxes[:, 2].clamp_(0, shape[1])  # x2
        boxes[:, 3].clamp_(0, shape[0])  # y2
    else:  # np.array (faster grouped)
        boxes[:, [0, 2]] = boxes[:, [0, 2]].clip(0, shape[1])  # x1, x2
        boxes[:, [1, 3]] = boxes[:, [1, 3]].clip(0, shape[0])  # y1, y2

def detect_color(xyxy, im, file='image.jpg', gain=1.02, pad=10, square=False, BGR=False, save=True):
    # Save image crop as {file} with crop size multiple {gain} and {pad} pixels. Save and/or return crop
    xyxy = torch.tensor(xyxy).view(-1, 4)
    b = xyxy2xywh(xyxy)  # boxes
    if square:
        b[:, 2:] = b[:, 2:].max(1)[0].unsqueeze(1)  # attempt rectangle to square
    b[:, 2:] = b[:, 2:] * gain + pad  # box wh * gain + pad
    xyxy = xywh2xyxy(b).long()
    clip_coords(xyxy, im.shape)
    crop = im[int(xyxy[0, 1]):int(xyxy[0, 3]), int(xyxy[0, 0]):int(xyxy[0, 2]), ::(1 if BGR else -1)]
    crop = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
    clt = KMeans(n_clusters=5)
    clt_1 = clt.fit(crop.reshape(-1, 3))
    color = color_cluster_priority(clt_1)
    return color

def draw_rectangle(event, x, y, flags, params):
    global x_init, y_init, drawing
    def update_pts():
        params["top_left_pt"] = (min(x_init, x), min(y_init, y))
        params["bottom_right_pt"] = (max(x_init, x), max(y_init, y))
        img[y_init:y, x_init:x] = 255 - img[y_init:y, x_init:x]
    if event == cv2.EVENT_LBUTTONDOWN:
        print('PIX:', x, y)
        print("BGR:", img[y, x])
        # print("GRAY:", gray[y, x])
        # print("HSV:", hsv[y, x])
        drawing = True
        x_init, y_init = x, y
    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        update_pts()
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        update_pts()
    elif event == cv2.EVENT_RBUTTONUP:
        img_crop = img_src[y0:y1, x0:x1]
        img_crop = cv2.cvtColor(img_crop, cv2.COLOR_BGR2RGB)
        start = time.time()
        clt = KMeans(n_clusters=5)
        clt_1 = clt.fit(img_crop.reshape(-1, 3))
        color = color_cluster_priority(clt_1)
        end = time.time()
        print('using time: ', end - start)
        print("the color most likely", color)
        # for idx, centers in enumerate(clt_1.cluster_centers_):
        #     hsv = rgb2hsv(centers[0], centers[1], centers[2])
        #     color_enum(hsv)
        show_img_compar(img_crop, palette_perc(clt_1))


def image_select():
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()

    #FolderPath=filedialog.askdirectory() #如果有特殊需要，非要选择文件夹，这个可以去掉注释使用
    FilePath=filedialog.askopenfilename() #一般这个直接选择文件，会比较符合人们的使用习惯和软件的用户体验

    # print('FolderPath:',FolderPath)
    print('FilePath:',FilePath)
    return FilePath

if __name__ == '__main__':
    drawing = False
    event_params = {"top_left_pt": (-1, -1), "bottom_right_pt": (-1, -1)}

    path_image = r"F:\share\video\qd3\light-detect\rail-car-day\rail-car-day-00025.jpg"
    path_image = image_select()
    img_src = cv2.imread(path_image)
    img_src = cv2.resize(img_src, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)


    img_src = cv2.cvtColor(img_src, cv2.COLOR_BGR2RGB)
    clt = KMeans(n_clusters=5)
    clt_1 = clt.fit(img_src.reshape(-1, 3))
    color = color_cluster_priority(clt_1)
    print(color)
    # exit(0)

    cv2.namedWindow('img')
    cv2.setMouseCallback('img', draw_rectangle, event_params)

    while True:
        img = img_src.copy()
        (x0, y0), (x1, y1) = event_params["top_left_pt"], event_params["bottom_right_pt"]
        img[y0:y1, x0:x1] = 255 - img[y0:y1, x0:x1]
        cv2.imshow('img', img)

        c = cv2.waitKey(1)
        if c == 27:
            break

    cv2.destroyAllWindows()


