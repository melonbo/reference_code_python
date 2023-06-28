import cv2
import os
from bs4 import BeautifulSoup


def annotation_from_xml(image_name, annotation_file):
    with open(annotation_file) as f:
        soup = BeautifulSoup(f)
        im = cv2.imread(image_name)
        bndboxs = soup.findAll('bndbox')
        for bndbox in bndboxs:
            xmin = bndbox.xmin.text
            ymin = bndbox.ymin.text
            xmax = bndbox.xmax.text
            ymax = bndbox.ymax.text
            im_out = cv2.rectangle(im, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 3)

        cv2.imshow(image_name, im_out)
        cv2.waitKey(0)


annotation_file_ = os.path.join(os.getcwd(), 'res', '00a290dc3ec3a138dd628a07a1ada8d6.xml')
image_name_ = os.path.join(os.getcwd(), 'res', '00a290dc3ec3a138dd628a07a1ada8d6.jpg')
annotation_from_xml(image_name_, annotation_file_)