import math

import cv2
import mpmath
import numpy as np


#     * * * * *
#     * * * * *
#     * * 0 * *
#     * * * * *
#     * * * * *

def neighbour_points(img_shape, center, distance):
    bag = []
    w = img_shape[1]
    h = img_shape[0]
    for i in range(center[0]-distance, center[0]+distance+1):
        for j in range(center[1]-distance, center[1]+distance+1):
            if i>=0 and j>=0 and i<h and j<w:
                bag.append((i,j))
    bag.remove(center)
    return bag


def get_loc_by_distance(x, y, distance) -> list:
    sec_list = []
    print("BEGIN :" + str(distance))
    seq = 0
    while distance >= 0:
        sec_list.append([x + distance, y + seq])
        if distance != 0:
            sec_list.append([x - distance, y + seq])
        if seq != 0:
            sec_list.append([x + distance, y - seq])
        if distance != 0 and seq != 0:
            sec_list.append([x - distance, y - seq])
        seq += 1
        distance -= 1
    return sec_list


def getPoint(bag):
    try:
        point = bag.pop()
        return point
    except:
        print('bag is enmpty to pop')
        return None


def calc_distace(p1, p2):
    distace = np.sqrt(np.sum(np.square(p1-p2)))
    p1_h, p1_s, p1_v = rgb2hsv(p1[0], p1[1], p1[2])
    p2_h, p2_s, p2_v = rgb2hsv(p2[0], p2[1], p2[2])
    # distace = np.sqrt(2*np.square(p1_h-p2_h)+0.5*np.square(p1_s-p2_s)+0.5*np.square(p1_v-p2_v))
    # print('distance', distace)
    return distace


def get_center_color_mean(img,center,distance,dst):
    neighbours = neighbour_points(img.shape, center, distance)
    neighbours.append(center)
    nei_valid = []
    b,g,r=0,0,0
    while len(neighbours):
        point = neighbours.pop()
        if dst[point[0], point[1]].tolist() == color_mark:
            nei_valid.append(point)
            b += img[point][0]
            g += img[point][1]
            r += img[point][2]
    size = len(nei_valid)
    return [b/size,g/size,r/size]


def rgb2hsv(b, g, r):
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


def find_lane(img, start):
    bag = []
    lane_points = []
    img_mask = np.zeros(img.shape[:2])
    img_dst = np.zeros_like(img)
    bag.append(start)
    img_mask[start] = 1;
    img_dst[start] = color_mark
    x_valid = 0

    while len(bag):
        center = getPoint(bag)
        if center:
            # print('get a point', center)
            neighbours = neighbour_points(img.shape, center, 1)
            neighbours2 = neighbour_points(img.shape, center, 5)
            neighbours3 = []
            while len(neighbours2):
                point = neighbours2.pop()
                if img_mask[point] == 1:
                    neighbours3.append(point)
            # line = None
            # if len(neighbours3)>100:
            #     line = fit_poly1d(neighbours3)


            # print('bag size', len(bag))
            # print('neighbour size %d, bag size %d'% (len(neighbours3), len(bag)))
            while len(neighbours):
                point = neighbours.pop()
                if img_mask[point] == 1:
                    continue
                else:
                    img_mask[point] = 1;

                if len(neighbours3):
                    x_valid = calc_distance_to_points_x(point, neighbours3)
                else:
                    x_valid = 0

                color_center = get_center_color_mean(img, center, 5, img_dst)
                distance = calc_distace(color_center, img[point[0], point[1]])

                if distance < 30 and x_valid < 4:
                    bag.append(point)
                    img_dst[point] = color_mark
                    lane_points.append(point)
    return lane_points


def fit_lane(img, lane_points):
    x_left = []
    y_left = []
    for i, item in enumerate(lane_points):
        x_left.append(item[1])
        y_left.append(item[0])
    z1 = np.polyfit(y_left, x_left, 2)
    p1 = np.poly1d(z1)
    for y in range(img.shape[0]):
        x= p1(y)
        if x<img.shape[1]:
            img[y,int(x)] = color_mark
    return p1


def fit_poly1d(points):
    # print('points ', points)
    x_left = []
    y_left = []
    for i, item in enumerate(points):
        x_left.append(item[1])
        y_left.append(item[0])
    z1 = np.polyfit(y_left, x_left, 1)
    p1 = np.poly1d(z1)
    return p1


def calc_distance_to_line(line, point):
    if not line:
        return
    x = line(point[0])
    angle = 1/math.atan(line[1])
    d = math.sin(angle)*(math.fabs(x-point[1]))
    print('line ', line[0], line[1])
    print('x angle d', x, angle, d)
    exit(0)

def calc_distance_to_points_x(point, points):
    x = 0
    for i,p in enumerate(points):
        x += p[1]

    return (abs(point[1]-x/len(points)))

def calc_distance(img, poly1d_left, poly1d_right):
    bag_x = []
    bag_y = []
    distance = 0
    for i in range(520, img.shape[0]):
        dis = poly1d_right(i) - poly1d_left(i)
        bag_x.append(i)
        bag_y.append(dis)
        distance += 1435 / dis
    z1 = np.polyfit(bag_x, bag_y, 2)
    print(distance / 100)


def mouse_event(event, x, y, flags, params):
    global start, start2
    if event == cv2.EVENT_LBUTTONDOWN:
        print('PIX:', x, y)
        if not start:
            start = (y,x)
        elif not start2:
            start = None
            start2 = (y,x)


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

# path = r"F:\share\video\qd3\light-detect\rail-car-day\rail-car-day-00025.jpg"
path = r"F:\share\video\qd3\light-detect\rail-car-night\rail-car-night-00025.jpg"
path = image_select()
img = cv2.imread(path)
img = cv2.resize(img, None, fx=1.0, fy=1.0, interpolation=cv2.INTER_AREA)
img = cv2.GaussianBlur(img, (3,3), 2, 1)
print('image shape', img.shape)
# PIX(x,y): 476 534
# BGR: [ 79  82 101]
start = (536, 476)
start2 = (520,685)
color_mark = [0,0,255]
stand_lane_distance = 1435

# lane_left = find_lane(img, start)
# poly1d_left = fit_lane(img, lane_left)
#
# lane_right = find_lane(img, start2)
# poly1d_right = fit_lane(img, lane_right)
#
# calc_distance(img, poly1d_left, poly1d_right)


# PIX(x,y): 476 534
# cv2.imshow('dst', img)
# cv2.waitKey()

cv2.namedWindow('img')
cv2.setMouseCallback('img', mouse_event)
start = None
start2 = None
print('click to select a start point')
while True:
    if start:
        lane_left = find_lane(img, start)
        img_copy = img.copy()
        for i, item, in enumerate(lane_left):
            img_copy[item] = color_mark
        cv2.imshow('img_copy', img_copy)
        cv2.waitKey(0)
        poly1d_left = fit_lane(img, lane_left)
        print(poly1d_left)
        start = None
    cv2.imshow('img', img)

    c = cv2.waitKey(1)
    if c == 27:
        break

cv2.destroyAllWindows()