import cv2
import numpy as np

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

def mouse_event(event, x, y, flags, params):
    global start
    if event == cv2.EVENT_LBUTTONDOWN:
        print('PIX:', x, y)
        start = (x,y)


path = image_select()
img = cv2.imread(path)
img = cv2.resize(img, None, fx=1.0, fy=1.0, interpolation=cv2.INTER_AREA)
img = cv2.GaussianBlur(img, (3,3), 2, 1)

cv2.namedWindow('img')
cv2.setMouseCallback('img', mouse_event)
start = None
diff = (30,30,30)
print('click to select a start point')
while True:
    if start:
        print('point color is ', img[start[0], start[1]])
    copyImg = img.copy()
    h, w = img.shape[:2]
    mask = np.zeros([h + 2, w + 2], np.uint8)  # mask必须行和列都加2，且必须为uint8单通道阵列
    cv2.floodFill(copyImg, mask, start, (0, 255, 255), diff, diff, cv2.FLOODFILL_FIXED_RANGE)

    cv2.imshow('img', copyImg)

    c = cv2.waitKey(1)
    if c == 27:
        break

cv2.destroyAllWindows()
