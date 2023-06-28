# coding:utf-8

# tkinter是Python内置的简单GUI库，实现打开文件夹、确认删除等操作十分方便
from tkinter.filedialog import askdirectory
# 导入创建的工具类
from opencv.picture.SimpleBBoxLabeling import SimpleBBoxLabeling

if __name__ == '__main__':
    dir_with_images = askdirectory(title='Where is the images?')
    labeling_task = SimpleBBoxLabeling(dir_with_images)
    labeling_task.start()
