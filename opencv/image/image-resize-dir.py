import os
import glob
from PIL import Image
import os.path
import sys


def convertjpg(jpgfile,savedir,width=500,height=400):
    img=Image.open(jpgfile)
    new_img=img.resize((width,height),Image.BILINEAR)
    new_img.save(os.path.join(savedir,os.path.basename(jpgfile)))


def resizeDir(fileSrc,saveDir):
    for jpgfile in glob.glob(fileSrc):
        print(jpgfile)
        convertjpg(jpgfile,saveDir)


if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print("param error")
        # sys.exit()
        file = r'*.jpg'
        saveDir = r'image_save_path'
        resizeDir(file,saveDir)
    else:
        resizeDir(sys.argv[1], sys.argv[2])