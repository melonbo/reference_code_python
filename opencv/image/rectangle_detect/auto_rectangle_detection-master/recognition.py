#!/usr/bin/python
from PIL import Image
import cv2
import numpy as np
import pytesseract
import re
import sys

def perspective_transformation(path):
    '''
    Usage : perspective_transformation(path) 
    path = [path to your picture]
    takes a picture as an input and return a transformed picture in your current workspace as output
    '''
    img = cv2.imread(path)
    
    pts1 = np.float32([[314,192],[524,197],[308,355],[521,356]])
    pts2 = np.float32([[0,0],[300,0],[0,300],[300,300]])
    M = cv2.getPerspectiveTransform(pts1,pts2)
    dst = cv2.warpPerspective(img,M,(300,300))
    return cv2.imwrite('transformation.png',dst)
    
def get_sensor_type(text):
    '''
    Usage : get_sensor_type(text)
    text should be a read 
    returns if the sensor is a multi_flex or an Evo, can add more sensor type in the future
    '''
    text=text.replace(" ","")
    text = filter(lambda x:  not re.match(r'^\s*$', x), text)
    sensor_type = text[text.find("T"):text.find("T")+5]
    if sensor_type == "TRMFX":
        return "TeraRanger Multi_flex"
    elif sensor_type == "TREVO":
        return "TeraRanger Evo"
    else:
        print ("### Error! sensor type no recognized !###")
        return 0

def get_serial_num(text):
    '''
    Usage : get_serial_num(text)
    text should be a read 
    returns the sensor's serial number
    '''
    text=text.replace(" ","")
    text = filter(lambda x:  not re.match(r'^\s*$', x), text)
    serial_num = text[text.find("T")+5:]
    return serial_num

def get_info(text):
    '''
    Usage : get_serial_num(text)
    text should be a read 
    returns the protocol of the sensor
    exmaple: TRMFX SN 17050083
    '''
    text=text.replace(" ","")
    text = filter(lambda x:  not re.match(r'^\s*$', x), text)
    sensor_type = text[text.find("T"):text.find("T")+5]
    serial_num = text[text.find("T")+5:]
    return sensor_type + " "+ "SN" + " " + serial_num

