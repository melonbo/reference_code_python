import os


# 目录下文件列表
def getNameList(dir, outputFile):
    files = os.listdir(dir)
    with open(outputFile, 'w') as f:
        for file in files:
            # print(os.path.splitext(file)[0])
            f.write(os.path.splitext(file)[0] + '\n')

# 遍历目录下文件
def listfiles(rootDir):
  list_dirs = os.walk(rootDir)
  for root, dirs, files in list_dirs:
    for d in dirs:
      print(os.path.join(root,d))
    for f in files:
      fileid = f.split('.')[0]
      filepath = os.path.join(root,f)
      print(filepath)
