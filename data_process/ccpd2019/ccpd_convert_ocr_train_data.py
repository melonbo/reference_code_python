import os
import re
import cv2
import string


input_path = r'E:\work\dataset\CCPD2019\ccpd_base_02.txt'
output_path = r'E:\work\dataset\CCPD2019\ccpd_base_02_ocr_train.txt'
provinces = ["皖", "沪", "津", "渝", "冀", "晋", "蒙", "辽", "吉", "黑", "苏", "浙", "京", "闽", "赣", "鲁", "豫", "鄂", "湘", "粤", "桂",
             "琼", "川", "贵", "云", "藏", "陕", "甘", "青", "宁", "新", "警", "学", "O"]

ads = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
       'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'O']

with open(output_path, 'w', encoding='utf-8') as f_out:
    with open(input_path,'r', encoding='utf-8') as f_in:
        for line in f_in.readlines():
            name = os.path.split(line)[-1].rstrip()
            ocr_group = line.split('-')[4]
            ocrs = ocr_group.split('_')
            # ocrs[0] = str(int(ocrs[0]) + 1)
            ocrs[0] = provinces[int(ocrs[0])]
            for i, ocr in enumerate(ocrs[1:]):
                # ocrs[i+1] = str(int(ocr)+35)
                ocrs[i + 1] = ads[int(ocr)]
            out_str=name + ' ' + ''.join(ocrs) + '\n'
            f_out.write(out_str)

# with open(output_path, 'w') as f_out:
#     with open(input_path,'r',encoding='utf-8') as f_in:
#         for line in f_in.readlines():
#             # print(line)
#             name = os.path.split(line)[-1].rstrip()
#             ocr_group = line.split('-')[4]
#             ocrs = ocr_group.split('_')
#             ocrs[0] = str(int(ocrs[0]) + 1)
#             for i, ocr in enumerate(ocrs[1:]):
#                 ocrs[i+1] = str(int(ocr)+35)
#             out_str=name + ' ' + ' '.join(ocrs) + '\n'
#             print(out_str)
            # f_out.write(out_str)
