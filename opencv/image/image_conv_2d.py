import matplotlib.pyplot as plt
import pylab
import numpy as np
import time


def timeit(func):
    def wrapper(img, fil, mode):
        start = time.clock()
        func(img, fil, mode)
        end = time.clock()
        print('time use %d'%(end-start))
    return wrapper

# @timeit
def convolve(img, fil, mode='same'):
    if mode == 'fill':
        h = fil.shape[0]
        w = fil.shape[1]
        img = np.pad(img, ((h,h),(w,w),(0,0)), 'constant')
    conv_b = _convolve(img[:,:,0], fil)
    conv_g = _convolve(img[:,:,1], fil)
    conv_r = _convolve(img[:,:,2], fil)

    dstack = np.dstack([conv_b, conv_g, conv_r])
    return dstack

def _convolve(img, fil):
    fil_heigh = fil.shape[0]
    fil_width = fil.shape[1]

    conv_heigh = img.shape[0] - fil.shape[0] + 1
    conv_width = img.shape[1] - fil.shape[1] + 1

    conv = np.zeros((conv_heigh, conv_width), dtype='uint8')

    for i in range(conv_heigh):
        for j in range(conv_width):
            conv[i][j] = wise_element_sum(img[i:i + fil_heigh, j:j + fil_width], fil)
    return conv

def wise_element_sum(img, fil):
    res = (img * fil).sum()
    if (res < 0):
        res = 0
    elif res > 255:
        res = 255
    return res



#卷积核应该是奇数行，奇数列的
fil = np.array([[-1,0,1],
                 [-2,0,2],
                 [-1,0,1]])

path = r"F:\share\video\qd3\QD3-003-01-20220516-210000.mp4_002904.033.jpg"
img = plt.imread(path)
res = convolve(img,fil,'fill')
print(type(res))
print(res.shape)
plt.imshow(res)
pylab.show()