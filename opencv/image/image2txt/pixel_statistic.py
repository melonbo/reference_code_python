import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import sys


def statistics(file):
    src = cv.imread(file)
    # cv.imshow("q",src)
    h, w, ch = np.shape(src)
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    # cv.imshow("gray", gray)
    hest = np.zeros([256], dtype=np.int32)
    for row in range(h):
        for col in range(w):
            pv = gray[row, col]
            hest[pv] += 1
    plt.plot(hest, color="r")
    plt.xlim([0, 256])
    plt.show()
    cv.waitKey(0)
    cv.destroyAllWindows()

if len(sys.argv) == 2:
    statistics(sys.argv[1])
else:
    statistics("1.jpg")
