import cv2
import numpy as np
import matplotlib.pyplot as plt

path = r"1.jpg"

img = cv2.imread(path)
img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

hsv_red_min_01=np.array([0,43,46])#红色阈值下界
hsv_red_max_01=np.array([10,255,255])#红色阈值上界
hsv_red_min_02=np.array([156,43,46])#红色阈值下界
hsv_red_max_02=np.array([180,255,255])#红色阈值上界
hsv_green_min=np.array([35,43,46])#绿色阈值下界
hsv_green_max=np.array([77,255,255])#绿色阈值上界
hsv_yellow_min = np.array([26, 43, 46])#黄色阈值下界
hsv_yellow_max = np.array([34, 255, 255])#黄色阈值上界
hsv_blue_min = np.array([100, 43, 46])#蓝色阈值下界
hsv_blue_max = np.array([124, 255, 255])#蓝色阈值上界
hsv_white_min = np.array([0, 0, 221])#白色阈值下届
hsv_white_max = np.array([180, 30, 255])#白色阈值上届
hsv_black_min = np.array([0, 0, 0])#白色阈值下届
hsv_black_max = np.array([180, 255, 46])#白色阈值上届
hsv_gray_min = np.array([0, 0, 46])#灰色阈值下届
hsv_gray_max = np.array([180, 43, 220])#灰色阈值上届
hsv_orange_min = np.array([11, 43, 46])#橙色阈值下届
hsv_orange_max = np.array([25, 255, 255])#橙色阈值上届
hsv_cyan_min = np.array([78, 43, 46])#青色阈值下届
hsv_cyan_max = np.array([99, 255, 255])#青色阈值上届
hsv_purple_min = np.array([125, 43, 46])#紫色阈值下届
hsv_purple_max = np.array([155, 255, 255])#紫色阈值上届

rgb_red_min = np.array([0, 5, 150])
rgb_red_max = np.array([8, 255, 255])
rgb_red_min2 = np.array([175, 5, 150])
rgb_red_max2 = np.array([180, 255, 255])
rgb_yellow_min = np.array([20, 5, 150])
rgb_yellow_max = np.array([30, 255, 255])
rgb_green_min = np.array([35, 50, 150])
rgb_green_max = np.array([90, 255, 255])

def color_detect(hsv):
    if inRangeList(hsv, hsv_red_max_01, hsv_red_min_01):
        print('红色01')
    if inRangeList(hsv, hsv_red_max_02, hsv_red_min_02):
        print('红色02')
    if inRangeList(hsv, hsv_green_max, hsv_green_min):
        print('绿色')
    if inRangeList(hsv, hsv_blue_max, hsv_blue_min):
        print('蓝色')
    if inRangeList(hsv, hsv_yellow_max, hsv_yellow_min):
        print('黄色')
    if inRangeList(hsv, hsv_white_max, hsv_white_min):
        print('白色')
    if inRangeList(hsv, hsv_black_max, hsv_black_min):
        print('黑色')
    if inRangeList(hsv, hsv_gray_max, hsv_gray_min):
        print('灰色')
    if inRangeList(hsv, hsv_orange_max, hsv_orange_min):
        print('橙色')
    if inRangeList(hsv, hsv_cyan_max, hsv_cyan_min):
        print('青色')
    if inRangeList(hsv, hsv_purple_max, hsv_purple_min):
        print('紫色')

def mouse_click(event, x, y, flags, para):
    if event == cv2.EVENT_LBUTTONDOWN:  # 左边鼠标点击
        print('PIX:', x, y)
        # print("BGR:", img[y, x])
        # print("GRAY:", gray[y, x])
        # print("HSV:", hsv[y, x])
        color_detect(hsv[y,x])
        print(2*x,2*y)

def main_01():
    cv2.namedWindow("img")
    cv2.setMouseCallback("img", mouse_click)
    while True:
        cv2.imshow('img', img)
        if cv2.waitKey() == ord('q'):
            break
    cv2.destroyAllWindows()

def square_color():
    h = img.shape[0]
    w = img.shape[1]
    sb = img[0, :, 0].sum() + img[h-1, :, 0].sum() + img[:, 0, 0].sum() + img[:, w-1, 0].sum()
    sb = sb/(w+w+h+h-4)
    sg = img[0, :, 1].sum() + img[h-1, :, 1].sum() + img[:, 0, 1].sum() + img[:, w-1, 1].sum()
    sg = sg/(w+w+h+h-4)
    sr = img[0, :, 2].sum() + img[h-1, :, 2].sum() + img[:, 0, 2].sum() + img[:, w-1, 2].sum()
    sr = sr/(w+w+h+h-4)
    print(sb, sg, sr)
    return sb, sg, sr

def inRangeList(arr, up, low):
    size = len(arr)
    for i in range(size):
        if arr[i] > up[i]:
            return False
        if arr[i] < low[i]:
            return False
    return True


if __name__ == '__main__':
    main_01()
    # square_color()
    # print(inRangeList((1,128,129), higher_red, lower_red))


    # cv2.imshow('', img)
    # cv2.waitKey(0)
    # cv2.imshow('', mask_red)
    # cv2.waitKey(0)