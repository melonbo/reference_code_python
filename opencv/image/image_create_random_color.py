import cv2
import numpy as np
import random


def random_image_color():
    img_shape = [200, 200, 3]
    img_color = [random.randrange(256), random.randrange(256), random.randrange(256)]
    img = np.zeros(img_shape, np.uint8)
    img = cv2.rectangle(img,(50, 50), (150, 150), img_color, 10)
    cv2.line(img, (0, 0), (200, 200), img_color)
    cv2.imshow('image', img)


while True:
    random_image_color()
    cv2.waitKey(1000)

