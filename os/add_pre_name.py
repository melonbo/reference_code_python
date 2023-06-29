import os
import shutil

path=r'/data/'
result = os.listdir(path)

for dir in result:
    if os.path.isdir(os.path.join(path, dir)):
        res = os.listdir(os.path.join(path, dir))
        for file in res:
            if os.path.splitext(file)[1] == '.mp4':
                input = os.path.join(path, dir, file)
                output = os.path.join(path, dir, "pre " + file)
                print(input)
                print(output)
                shutil.move(input, output)