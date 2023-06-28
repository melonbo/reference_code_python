#!/usr/bin/python

from recognition import *

f_name = sys.argv[1]
perspective_transformation(f_name)
img = 'transformation.png'
text = pytesseract.image_to_string(Image.open(img))
print (get_sensor_type(text))
print (get_serial_num(text))
print (get_info(text))

