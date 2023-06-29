#!/usr/bin/env python
# coding:utf-8

# from xml.etree.ElementTree import Element, SubElement, tostring
from lxml.etree import Element, SubElement, tostring
from xml.dom.minidom import parseString
import os
import cv2
import numpy as np
import sys


def toPascalvocXml(image_folder, file_name, file_size, obj_list, class_name_list):
    node_root = Element('annotation')

    node_folder = SubElement(node_root, 'folder')
    node_folder.text = image_folder

    node_filename = SubElement(node_root, 'filename')
    node_filename.text = file_name

    node_size = SubElement(node_root, 'size')
    node_width = SubElement(node_size, 'width')
    node_width.text = str(file_size[0])

    node_height = SubElement(node_size, 'height')
    node_height.text = str(file_size[1])

    node_depth = SubElement(node_size, 'depth')
    node_depth.text = str(file_size[2])

    for i in range(len(obj_list)):
        node_object = SubElement(node_root, 'object')
        node_name = SubElement(node_object, 'name')
        class_name_id = int(obj_list[i][0])
        node_name.text = class_name_list[class_name_id]

        node_difficult = SubElement(node_object, 'difficult')
        node_difficult.text = '0'
        node_bndbox = SubElement(node_object, 'bndbox')
        node_xmin = SubElement(node_bndbox, 'xmin')
        node_xmin.text = str(obj_list[i][1])
        node_ymin = SubElement(node_bndbox, 'ymin')
        node_ymin.text = str(obj_list[i][2])
        node_xmax = SubElement(node_bndbox, 'xmax')
        node_xmax.text = str(obj_list[i][3])
        node_ymax = SubElement(node_bndbox, 'ymax')
        node_ymax.text = str(obj_list[i][4])

    xml = tostring(node_root, pretty_print=True)  # 格式化显示，该换行的换行
    dom = parseString(xml)
    xml_file=os.path.splitext(file_name)[0]+'.xml'

    return xml


def read_annotation(name):
    obj_list = []
    with open(name, 'rb') as f:
        for line in f.readlines():
            line=line.decode()
            line=line.replace('\r', '').replace('\n', '').split(' ')
            obj_list.append(line)
    return(obj_list)

def read_class_name_list(class_name_file):
    class_name_list = []
    with open(class_name_file) as file:
        for classes in file:
            class_name_list.append(classes)
    return class_name_list

def start_process(annotation_dir, img_dir, xml_dir, image_folder, class_name_file):
    if not os.path.isdir(xml_dir):
        os.mkdir(xml_dir)
    else:
        for file in os.listdir(xml_dir):
            os.remove(os.path.join(xml_dir,file))

    for file in os.listdir(annotation_dir):
        annotation_name=file
        annotation_name_full=os.path.join(annotation_dir, annotation_name)
        annotation_name_xml=annotation_name.replace('txt', 'xml')
        img_name=annotation_name.replace('txt', 'jpg')
        img_name_full=os.path.join(img_dir, img_name)
        # print(img_name_full)
        img=cv2.imdecode(np.fromfile(img_name_full,dtype=np.uint8),cv2.IMREAD_COLOR)

        file_size=(img.shape[1], img.shape[0], img.shape[2])

        obj_list=read_annotation(annotation_name_full)
        class_name_list = read_class_name_list(class_name_file)
        xml = toPascalvocXml(image_folder, img_name, file_size, obj_list, class_name_list)

        with open(os.path.join(xml_dir, annotation_name_xml), "w") as f:
            f.write(str(xml, encoding="utf-8"))

'''
annotation_dir='/media/linc/data1/data_set/安检-充电宝/遮挡问题/coreless_3000/Annotation'
img_dir='/media/linc/data1/data_set/安检-充电宝/遮挡问题/coreless_3000/Image'
xml_dir='./VOC2012/Annotations'
folder='VOC2012'
'''
annotation_dir=r'E:\work\dataset\BrainWash\brainwash_yolo\labels'
img_dir=r'E:\work\dataset\BrainWash\brainwash_yolo\JPEGImages'
xml_dir=r'E:\work\dataset\BrainWash\brainwash_yolo\Annotations'
image_folder_string='JPEGImages'
class_name_file=r'E:\work\dataset\BrainWash\brainwash_yolo\yolo3_object.names'


if __name__ == '__main__':
    if len(sys.argv) == 6:
        annotation_dir = sys.argv[1]
        annotation_dir = os.path.abspath(annotation_dir)
        img_dir = sys.argv[2]
        img_dir = os.path.abspath(img_dir)
        xml_dir = sys.argv[3]
        xml_dir = os.path.abspath(xml_dir)
        image_folder_string = sys.argv[4]
        class_name_file = sys.argv[5]
        class_name_file = os.path.abspath(class_name_file)
    else:
        print("use defalut args")

    print(annotation_dir, img_dir, xml_dir, image_folder_string, class_name_file)

    start_process(annotation_dir, img_dir, xml_dir, image_folder_string, class_name_file)