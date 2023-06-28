# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os,sys,types
import matplotlib.pyplot as plt
import datetime
import csv
import codecs
import xlwt

#均值哈希算法
def aHash(image):
    image_new = image
    #计算均值
    average = np.mean(image_new)
    hash = []
    for i in range(image_new.shape[0]):
        for j in range(image_new.shape[1]):
            if image[i][j] > average:
                hash.append(1)
            else:
                hash.append(0)
    return hash


#计算汉明距离
def Hamming_distance(hash1, hash2):
    try:
        bit_xor = np.bitwise_xor(int(hash1, 2)&0xffffffff, int(hash2, 2)&0xffffffff)
        return str(bin(bit_xor)).count('1')
    except:
        print('=======', hash1, hash2)
        return 0


def readImage(image_name):
    image = cv2.imread(image_name)
    image = cv2.resize(image, (8,8))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image


def show2image(image1, image2):
    img1 = cv2.imread(image1)
    img2 = cv2.imread(image2)
    plt.subplot(2, 1, 1)
    plt.imshow(img1)
    plt.subplot(2, 1, 2)
    plt.imshow(img2)
    plt.show()

def show2image2(path, image1, image2):
    img1 = cv2.imread(os.path.join(path,image1))
    img2 = cv2.imread(os.path.join(path,image2))
    plt.subplot(2, 1, 1)
    plt.imshow(img1)
    plt.subplot(2, 1, 2)
    plt.imshow(img2)
    plt.show()

def test2image():
    image1 = cv2.imread('1.jpg')
    image1 = cv2.resize(image1, (8,8))
    image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)

    image2 = cv2.imread('2.jpg')
    image2 = cv2.resize(image2, (8,8))
    image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    hash1 = aHash(image1)
    hash2 = aHash(image2)

    dist = Hamming_distance(hash1, hash2)

    #将距离转换为相似度
    similarity = 1 - dist*1.0/64
    print("distance=%d"%dist)
    print("similarity=%f"%similarity)

list_hash = []
images_name = []
def hashInDir(path):
    global images_name
    images_name = os.listdir(path)
    a = datetime.datetime.now()
    for i in range(len(images_name)):
    # for i in range(3):
        # print("image %d, %s"%(i+1, images_name[i]))
        image = readImage(os.path.join(path, images_name[i]))
        image_hash = aHash(image)
        list_hash.append(image_hash)
    b = datetime.datetime.now()
    print("calc ahash %d files, used time %d seconds"%(len(list_hash), (b-a).seconds))

def writeHashToFile(name):
    with open(name,'w',encoding='utf-8') as f:
        for i in range(len(list_hash)):
            f.write(images_name[i] + ' ' + ''.join(map(str, list_hash[i])) + "\n")

def writeDistToFile(name, dist_matrix):
    shape = np.shape(dist_matrix)
    with open(name, 'w', encoding='utf-8') as f:
        for i in range(shape[0]):
            f.write(' '.join(map(str, dist_matrix[i])))

def data_write_csv(file_name, datas):  # file_name为写入CSV文件的路径，datas为要写入数据列表
    file_csv = codecs.open(file_name, 'w+', 'utf-8')  # 追加
    writer = csv.writer(file_csv, delimiter=' ', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
    for data in datas:
        print(data)
        writer.writerow(data)


def data_write_excel(file_path, datas):
    f = xlwt.Workbook()
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet

    # 将数据写入第 i 行，第 j 列
    i = 0
    for data in datas:
        for j in range(len(data)):
            sheet1.write(i, j, data[j])
        i = i + 1

    f.save(file_path)  # 保存文件

def removeDuplicates(name):
    list_image = []
    list_ahash = []
    dist_matrix = []
    dist_row = []
    with open(name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            section = line.split(' ')
            list_image.append(section[0])
            list_ahash.append(section[1])

    a = datetime.datetime.now()
    list_size = len(list_ahash)
    for i in range(list_size):
        dist_row.clear()
        b = datetime.datetime.now()
        for j in range(list_size):
            if j<=i:
                dist_row.append(0)
                continue
            else:
                dist = Hamming_distance(list_ahash[i], list_ahash[j])
                print('dist', dist)
                dist_row.append(dist)
                if dist < 6:
                    print(list_image[i] + ' | ' + list_image[j], dist)
        c = datetime.datetime.now()
        dist_matrix.append(dist_row)
    print("calc dist %d files, used time %d seconds" % (len(list_ahash), (c - a).seconds))


if __name__ == '__main__':
    # hashInDir(r"E:\image\bea-new-all")
    # writeHashToFile(os.path.join("E:\image", 'hash.txt'))
    removeDuplicates(r"E:\image\hash-base.txt")
