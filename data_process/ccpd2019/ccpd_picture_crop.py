import os
import cv2
import re


input_path = r'E:\work\dataset\CCPD2019\ccpd_base_02.txt'
output_path = r'E:\work\dataset\CCPD2019'

with open(input_path, 'r', encoding='utf-8') as f_in:
    for line in f_in.readlines():
        print(line)
        name = os.path.split(line)[-1].rstrip()
        pos_group = line.split('-')[2]
        print(pos_group)
        pos = re.split('[&_]',pos_group.strip())
        print(pos)
        output_file = os.path.join(output_path, name)
        print(output_file)
        img = cv2.imread(line)
        cropped = img[int(pos[1]):int(pos[3]), int(pos[0]):int(pos[2])]
        cv2.imwrite(output_file, cropped)
