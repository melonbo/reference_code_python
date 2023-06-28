import os


# 目录下文件列表
def getNameList(dir, outputFile):
    files = os.listdir(dir)
    with open(outputFile, 'w') as f:
        for file in files:
            # print(os.path.splitext(file)[0])
            f.write(os.path.splitext(file)[0] + '\n')


