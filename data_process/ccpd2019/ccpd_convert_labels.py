import os
import re
import cv2
import numpy as np


class_num = 0
input_path = r'E:\work\dataset\CCPD2019\ccpd_base'
output_path = r'E:\work\dataset\CCPD2019\ccpd_base'
input_full_name = r'E:\work\dataset\CCPD2019\ccpd_base\0072-0_1-432&512_566&557-565&556_432&557_433&513_566&512-0_0_8_30_32_29_10-126-14.jpg'

def test():
    file_base_name = os.path.basename(input_full_name)
    print(file_base_name)
    output_full_name = os.path.join(output_path, file_base_name.replace('jpg', 'txt'))

    annotation = file_base_name.split('-')[2]
    annotations = re.split('&|_', annotation)

    x1 = int(annotations[0])
    y1 = int(annotations[1])
    x2 = int(annotations[2])
    y2 = int(annotations[3])

    image = cv2.imread(input_full_name)
    h, w, ch = np.shape(image)

    x_center_norm = ((x2 + x1)/2)/w
    y_center_norm = ((y2 + y1)/2)/h
    w_norm = (x2 - x1)/w
    h_norm = (y2 - y1)/h

    str_out = str(class_num) + ' ' + str(x_center_norm) + ' ' + str(y_center_norm) + ' ' + str(w_norm) + ' ' + str(h_norm)

    with open(output_full_name, 'wb') as f:
        f.write(bytes(str_out, encoding='utf-8'))


for file in os.listdir(input_path):
    if file.endswith('.jpg'):
        input_full_name = os.path.join(input_path, file)
        output_full_name = os.path.join(output_path, file.replace('jpg', 'txt'))

        annotation = file.split('-')[2]
        annotations = re.split('&|_', annotation)

        x1 = int(annotations[0])
        y1 = int(annotations[1])
        x2 = int(annotations[2])
        y2 = int(annotations[3])

        image = cv2.imread(input_full_name)
        h, w, ch = np.shape(image)
        print("%d %d %d" %(h, w, ch))

        x_center_norm = ((x2 + x1) / 2) / w
        y_center_norm = ((y2 + y1) / 2) / h
        w_norm = (x2 - x1) / w
        h_norm = (y2 - y1) / h

        str_out = str(class_num) + ' ' + str(x_center_norm) + ' ' + str(y_center_norm) + ' ' + str(w_norm) + ' ' + str(
            h_norm)

        with open(output_full_name, 'wb') as f:
            f.write(bytes(str_out, encoding='utf-8'))
