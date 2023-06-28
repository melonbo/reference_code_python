import cv2
import numpy as np

# 原地址 https://www.zhuxianfei.com/python/56327.html
def unevenLightCompensate(gray, blockSize):
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    average = np.mean(gray)
    average = average*2
    rows_new = int(np.ceil(gray.shape[0] / blockSize))
    cols_new = int(np.ceil(gray.shape[1] / blockSize))
    blockImage = np.zeros((rows_new, cols_new), dtype=np.float32)
    for r in range(rows_new):
        for c in range(cols_new):
            rowmin = r * blockSize
            rowmax = (r + 1) * blockSize
            if (rowmax > gray.shape[0]):
                rowmax = gray.shape[0]
            colmin = c * blockSize
            colmax = (c + 1) * blockSize
            if (colmax > gray.shape[1]):
                colmax = gray.shape[1]
            imageROI = gray[rowmin:rowmax, colmin:colmax]
            temaver = np.mean(imageROI)

            blockImage[r, c] = temaver

    blockImage = blockImage - average
    blockImage2 = cv2.resize(blockImage, (gray.shape[1], gray.shape[0]), interpolation=cv2.INTER_CUBIC)
    gray2 = gray.astype(np.float32)
    dst = gray2 - blockImage2
    dst[dst > 255] = 255
    dst[dst < 0] = 0
    dst = dst.astype(np.uint8)
    dst = cv2.GaussianBlur(dst, (3, 3), 0)
    # dst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    return dst


if __name__ == '__main__':
    file = r"F:\share\video\qd3\QD3-003-01-20220516-210000.mp4_002904.033.jpg"
    blockSize = 8
    img = cv2.imread(file)
    b, g, r = cv2.split(img)
    dstb = unevenLightCompensate(b, blockSize)
    dstg = unevenLightCompensate(g, blockSize)
    dstr = unevenLightCompensate(r, blockSize)
    dst = cv2.merge([dstb, dstg, dstr])
    result = np.concatenate([img, dst], axis=1)
cv2.imwrite('result.jpg', result)