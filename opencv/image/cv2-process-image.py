import numpy as np
import cv2

# 显示图像
def image_show(src):
    pic = cv2.imread(src)
    cv2.imshow('', pic)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 灰度图
def picture_to_gray(src_pic, dst_pic):
    print(src_pic)
    print(dst_pic)
    lenna = cv2.imread(src_pic)
    row, col, channel = lenna.shape
    rgb_gray = np.zeros((row, col))
    for r in range(row):
        for l in range(col):
            rgb_gray[r, l] = 0.11 * lenna[r, l, 0] + 0.59 * lenna[r, l, 1] + 0.3 * lenna[r, l, 2]
            rgb_gray[r, l] = 255 - rgb_gray[r, l]
    # rgb_gray = cv2.inRange(rgb_gray, np.array([200,200,200]), np.array([255,255,255]))
    rgb_gray[rgb_gray < 50] = 0
    rgb_gray[rgb_gray > 50] = 255
    # cv2.imwrite(dst_pic, rgb_gray)
    # cv2.imshow("rgb_gray", rgb_gray.astype("uint8"))
    # cv2.waitKey()

# 调整尺寸
def image_resize(src, w, h):
    pic = cv2.imread(src)
    pic = cv2.resize(pic, (w,h), interpolation=cv2.INTER_CUBIC)
    return pic


# 二值图像
def image_binary(path):
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, img_thresh = cv2.threshold(gray,230, 255, cv2.THRESH_BINARY)
    cv2.imshow('', img_thresh)
    cv2.waitKey(0)


# 检测轮廓
def image_detect_contours(src):
    img = cv2.imread(src)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转成灰度图像
    ret, binary = cv2.threshold(gray,127,255,cv2.THRESH_BINARY) # 将灰度图像转成二值图像
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # 查找轮廓
    cv2.drawContours(img, contours, -1, (0, 0, 255), 3)
    cv2.imshow("img", img)
    cv2.waitKey(0)


# example image_adjust_brightness(r"1.jpg", brightness_factor=1.5)
def image_adjust_brightness(img_path, brightness_factor):
    img = cv2.imread(img_path)

    # clip(0, 255)会把处理后的像素值的大小，现在在[0, 255]范围内，如果有值大于255则取255,如果有值小于0则取值0
    table = np.array([i * brightness_factor for i in range (0,256)]).clip(0,255).astype('uint8')

    # 单通道img
    if img.shape[2] == 1:
        return cv2.LUT(img, table)[:,:,np.newaxis]
    # 多通道img
    else:
        result = cv2.LUT(img, table)
        # 左边原图、右边增加亮度后的图
        imgs_hstack = np.hstack((img, result))
        # cv2.imwrite("adjust_brightness_result.png", imgs_hstack)
        cv2.imshow("result", imgs_hstack)
        cv2.waitKey(0)
        return result


# 加矩形框
def image_add_rectangle(image, x1, y1, x2, y2, r, g, b, w):
    im = cv2.imread(image)
    cv2.rectangle(im, (int(x1), int(y1)), (int(x2), int(y2)), (r, g, b), w)
    return im


# 剪切
def image_crop(image):
    im = cv2.imread(image)
    im = im[1:470, 1:640]
    cv2.imshow('', im)
    cv2.waitKey(0)


# 图像差值
def image_minus(img_01, img_02):
    image1 = cv2.imread(img_01)
    image2 = cv2.imread(img_02)
    image3 = image1 - image2
    cv2.namedWindow("Image")
    cv2.imshow("Image", image3)
    cv2.waitKey(0)

