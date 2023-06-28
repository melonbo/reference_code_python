import requests


def downloadpicture(name, url):
    for j in range(1, 4):
        try:
            pic = requests.get(url, timeout=15)
            if pic.status_code == 200:
                with open(name, 'wb') as f:
                    f.write(pic.content)
                    print('成功下载图片: %s' % (str(url)))
                break
        except Exception as e:
            print(e)
            print('下载图片时失败: %s' % (str(url)))


filename = 'picture_url.txt'
with open(filename, 'rb') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        name='pictures/'+str(i)+'.jpg'
        array=line.decode().split('/')
        downloadpicture(name, line)