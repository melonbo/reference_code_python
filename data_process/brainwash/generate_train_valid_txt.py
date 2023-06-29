import os
import cv2
import glob
import random
import sys


label_path = r'E:\work\dataset\BrainWash\brainwash_yolo\JPEGImages'
train_val_path = r'E:\work\dataset\BrainWash\brainwash_yolo'

def split_dataset(label_path, train_val_path):
    train_txt = os.path.join(train_val_path, 'train.txt')
    valid_txt = os.path.join(train_val_path, 'val.txt')
    image_list = os.listdir(label_path)
    random.shuffle(image_list)
    num = len(image_list)

    #这里是划分，我设置的是0.85：0.15  可以根据自己情况划分
    train_list = image_list[:int(0.85*num)]
    val_list = image_list[int(0.85*num):]

    with open(train_txt,'w') as f:
        for line in train_list:
            jpg_name = line.replace('txt','jpg')
            jpg_name = os.path.join(train_val_path, jpg_name)
            f.write(jpg_name + '\n')

    with open(valid_txt,'w') as f:
        for line in val_list:
            jpg_name = line.replace('txt','jpg')
            jpg_name = os.path.join(train_val_path, jpg_name)
            f.write(jpg_name + '\n')

if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) == 3:
        label_path = sys.argv[1]
        train_val_path = sys.argv[2]
    else:
        print('use default args')

    print(label_path, train_val_path)
    split_dataset(label_path, train_val_path)


