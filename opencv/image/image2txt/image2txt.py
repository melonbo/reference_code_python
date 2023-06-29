from PIL import Image
import sys

image_name = "1.jpg"
thresh = ""
if len(sys.argv) == 3:
    image_name = sys.argv[1]
    thresh = int(sys.argv[2])
    print("number of arguments is %d" % (len(sys.argv)))
    print("file name : %s" % image_name)
    print("threshold : %d" % thresh)

image_text = image_name.split('.')[0] + ".txt"
print("image_text : %s" % image_text)

#打开图片
im = Image.open(image_name)
im = im.convert("L")

#获取图片宽和高
width = im.size[0]
height = im.size[1]
print("width=%d" % width)
print("height=%d" % height)

#将图片转化为文本，在每个像素点处用数字和空白字符替换
fh = open(image_text, 'w')
for i in range(height):
    for j in range(width):
        if i%1 == 0:
            col = im.getpixel((j, i))  #  获取(j,i)像素点颜色
            # print(col)
            # print(int(thresh))
            if col < int(thresh):
                fh.write('/')#在黑色像素点处用数字1代替
            else:
                fh.write(' ')#在非黑色像素点处用空格代替

            if j == width-1:
                fh.write('\n')
fh.close()

