#python png2jpg.py pngpath
import sys
from PIL import Image
import cv2 as cv
import os

pngpath=''
jpgpath=''

def convert_png_to_jpg(PngPath):
    if os.path.splitext(PngPath)[1] != '.png':
        return
    img = cv.imread(PngPath, -1)
    w, h = img.shape[:2]
    infile = PngPath
    outfile = os.path.splitext(infile)[0] + ".jpg"
    img = Image.open(infile)
    # img = img.resize((int(w / 2), int(h / 2)), Image.ANTIALIAS)
    try:
        if len(img.split()) == 4:
            # prevent IOError: cannot write mode RGBA as BMP
            r, g, b, a = img.split()
            img = Image.merge("RGB", (r, g, b))
            img.convert('RGB').save(outfile)
            os.remove(PngPath)
        else:
            img.convert('RGB').save(outfile)
            os.remove(PngPath)
        return outfile
    except Exception as e:
        print("PNG转换JPG 错误", e)


if __name__ == '__main__':
    print("start ...")
    if(len(sys.argv)==2):
        pngpath = sys.argv[1]

    if os.path.isfile(pngpath):
        convert_png_to_jpg(pngpath)
    if os.path.isdir(pngpath):
        files = os.listdir(pngpath)
        for file in files:
            full_path = os.path.join(pngpath, file)
            if os.path.isfile(full_path):
                print(full_path)
                convert_png_to_jpg(full_path)
