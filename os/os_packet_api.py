import os
import shutil


# 遍历文件夹
def find_files(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append(file_path)
    return file_list


# 文件名加前缀，前后目录相同
def add_prefix_to_filename(filename, prefix):
    filename_new = prefix + filename
    filename_old_abs = os.path.abspath(filename)
    filename_new_abs = os.path.abspath(filename_new)
    os.rename(filename_old_abs, filename_new_abs)


# 文件重命名，前后目录不同
def file_rename(filename_pre, filename_post):
    shutil.move(filename_pre, filename_post)





