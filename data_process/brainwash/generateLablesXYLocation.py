import os
import sys

idl_file_path = r"E:\work\dataset\BrainWash\brainwash\brainwash_train.idl"
label_txt_dir = r"E:\work\dataset\BrainWash\brainwash_yolo\labels"


def convert_file(idl_file_path, label_txt_dir):
    if not os.path.exists(label_txt_dir):
        os.mkdir(label_txt_dir)
    f1 = open(idl_file_path, 'r+')
    lines = f1.readlines()
    # print(range(len(lines)))

    for i in range(len(lines)):
        line = lines[i]
        line = line.replace(":", ";")
        # print(line)
        img_dir = line.split(";")[0]
        # print(img_dir)
        img_boxs = line.split(";")[1]
        img_dir = img_dir.replace('"', "")
        # print(img_dir)
        img_name = img_dir.split("/")[0]
        txt_name = img_name.split(".")[0]
        img_extension = img_name.split(".")[1]
        # print(txt_name)
        # print(img_extension)
        img_boxs = img_boxs.replace(",", "")
        # print(img_boxs)
        img_boxs = img_boxs.replace("(", "")
        img_boxs = img_boxs.split(")")
        # print(img_boxs)
        if (img_extension == 'jpg'):
            for n in range(len(img_boxs) - 1):
                box = img_boxs[n]
                box = box.split(" ")
                # print(box)
                # print(box[4])
                with open(label_txt_dir + "/" + txt_name + ".txt", 'a') as f:
                    f.write(' '.join(['0', str(float(box[1])), str(float(box[2])), str(float(box[3])), str(float(box[4]))]) + '\n')


if __name__ == '__main__':
    print("start ...")
    if len(sys.argv) == 3:
        idl_file_path = sys.argv[1]
        label_txt_dir = sys.argv[2]

    print(sys.argv)
    print(idl_file_path)
    print(label_txt_dir)

    if not os.path.isfile(idl_file_path):
        print("argv 1 error")
        exit()

    if not os.path.isdir(label_txt_dir):
        print("argv 2 error")
        exit()

    convert_file(idl_file_path, label_txt_dir)