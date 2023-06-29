#!/usr/bin/python
# -*- coding: UTF-8 -*-
# get annotation object bndbox location
import os
import cv2
import sys

try:
    import xml.etree.cElementTree as ET  # 解析xml的c语言版的模块
except ImportError:
    import xml.etree.ElementTree as ET


##get object annotation bndbox loc start
def GetAnnotBoxLoc(AnotPath):  # AnotPath VOC标注文件路径
    tree = ET.ElementTree(file=AnotPath)  # 打开文件，解析成一棵树型结构
    root = tree.getroot()  # 获取树型结构的根
    ObjectSet = root.findall('object')  # 找到文件中所有含有object关键字的地方，这些地方含有标注目标
    ObjBndBoxSet = {}  # 以目标类别为关键字，目标框为值组成的字典结构
    for Object in ObjectSet:
        ObjName = Object.find('name').text
        BndBox = Object.find('bndbox')
        x1 = float(BndBox.find('xmin').text)  # -1 #-1是因为程序是按0作为起始位置的
        y1 = float(BndBox.find('ymin').text)  # -1
        x2 = float(BndBox.find('xmax').text)  # -1
        y2 = float(BndBox.find('ymax').text)  # -1
        BndBoxLoc = [x1, y1, x2, y2]
        if ObjName in ObjBndBoxSet:
            ObjBndBoxSet[ObjName].append(BndBoxLoc)  # 如果字典结构中含有这个类别了，那么这个目标框要追加到其值的末尾
        else:
            ObjBndBoxSet[ObjName] = [BndBoxLoc]  # 如果字典结构中没有这个类别，那么这个目标框就直接赋值给其值吧
    return ObjBndBoxSet


##get picture size
def GetPictureSize(AnotPath):  # AnotPath VOC标注文件路径
    tree = ET.ElementTree(file=AnotPath)  # 打开文件，解析成一棵树型结构
    root = tree.getroot()  # 获取树型结构的根
    size = root.find('size')  # 找到文件中所有含有object关键字的地方，这些地方含有标注目标
    width = int(size.find('width').text)
    height = int(size.find('height').text)
    return (width, height)


##get object annotation bndbox loc end

def display(objBox, pic):
    img = cv2.imread(pic)
    width, height = 640, 480
    for key in objBox.keys():
        for i in range(len(objBox[key])):
            x1 = int(objBox[key][i][0]*width) - int(objBox[key][i][2]*width/2)
            y1 = int(objBox[key][i][1]*height) - int(objBox[key][i][3]*height/2)
            x2 = int(objBox[key][i][0] * width) + int(objBox[key][i][2] * width/2)
            y2 = int(objBox[key][i][1] * height) + int(objBox[key][i][3] * height/2)
            print(x1, y1)
            print(x2, y2)

            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(img, key, (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)
    cv2.imshow('img', img)
    cv2.imwrite('display.jpg', img)
    cv2.waitKey(0)


pic = r"E:\work\dataset\BrainWash\brainwash\brainwash_11_24_2014_images\00001000_640x480.jpg"
xml = r"E:\work\dataset\BrainWash\brainwash_yolo\Annotations\00001000_640x480.xml"

if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv)==3:
        pic = os.path.abspath(sys.argv[1])
        xml = os.path.abspath(sys.argv[2])
    else:
        print("use default args")

    print("picture is %s"%pic)
    print("xml file is %s"%xml)

    ObjBndBoxSet = GetAnnotBoxLoc(xml)
    GetPictureSize(xml)
    print(ObjBndBoxSet)
    display(ObjBndBoxSet, pic)
