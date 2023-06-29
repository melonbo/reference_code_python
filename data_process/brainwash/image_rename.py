import os
import sys
import shutil

src_path = r'E:\work\dataset\BrainWash\brainwash-xx\brainwash_11_24_2014_images'
dst_path = r'E:\work\dataset\BrainWash\brainwash_yolo\JPEGImages'
if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv)==3:
        src_path = sys.argv[1]
        dst_path = sys.argv[2]

    if not os.path.isdir(src_path):
        print("src path error")
        exit()
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)

    dir = os.path.split(src_path)[-1]
    files = os.listdir(src_path)
    for file in files:
        file_src = os.path.join(src_path, file)
        file_dst = dir + "_" + file
        file_dst = os.path.join(dst_path, file_dst)
        # print(file_src, file_dst)
        try:
            shutil.copyfile(file_src, file_dst)
        except OSError as err:
            print(err)
