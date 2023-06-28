
import cv2
import numpy as np
import sys
import os
import numpy as np
from matplotlib import pyplot as plt

def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )
	
def find_squares(vid):
	vid = cv2.GaussianBlur(vid, (5, 5), 0)
	squares = []
	for gray in cv2.split(vid):
		for thrs in xrange(0, 255, 26):
			if thrs == 0:
				edge = cv2.Canny(gray, 0, 50, apertureSize=5)
				edge = cv2.dilate(edge, None)
			else:
				retval, edge = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
			edge, contours, hierarchy = cv2.findContours(edge, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
			
			for cnt in contours:
				cnt_len = cv2.arcLength(cnt, True)
				cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
				if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
					cnt = cnt.reshape(-1, 2)
					max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
					if max_cos < 0.1:
						squares.append(cnt)
	return squares
def biggest_square(squares):
	biggestSquare = squares[0]
	for i in range(len(squares)):
		if (surface(squares[i]) > surface(biggestSquare)):
			biggestSquare = squares[i]
	return biggestSquare

def surface(square):
	a1 = square[2][0] - square[1][0]
	a2 = square[2][1] - square[1][1]
	a = np.sqrt(a1*a1 + a2*a2)
	b1 = square[1][0] - square[0][0]
	b2 = square[1][1] - square[0][1]
	b = np.sqrt(b1*b1 + b2*b2)
	return int(a)*int(b)

def transformation(img, squares):
	sq = biggest_square(squares)
	a1 = sq[2][0] - sq[1][0]
	a2 = sq[2][1] - sq[1][1]
	a = int(np.sqrt(a1*a1 + a2*a2))
	b1 = sq[1][0] - sq[0][0]
	b2 = sq[1][1] - sq[0][1]
	b = int(np.sqrt(b1*b1 + b2*b2))
	pts1 = np.float32([[sq[0][0],sq[0][1]],[sq[3][0],sq[3][1]],[sq[1][0],sq[1][1]],[sq[2][0],sq[2][1]]])
	pts2 = np.float32([[0,0],[a,0],[0,b],[a,b]])

	M = cv2.getPerspectiveTransform(pts1,pts2)
	dst = cv2.warpPerspective(img,M,(a,b))
	return dst

filepath = './data'
dstpath = './corrected'
frame = cv2.imread('88.jpg')
frame_2 = frame 
# squares = find_squares(frame)
# print squares[0], squares[0][0][0], squares[0][1], squares[0][2], squares[0][3]
# print biggestSquare
# cv2.imshow("frame", frame)
# dst = cv2.drawContours(frame, squares, -1, (0, 255, 0), 3 )
# dst = transformation(frame, squares)
# cv2.imwrite('transformation.png',dst)
# cv2.imshow('squares', dst)
# k = cv2.waitKey(0)

squares = find_squares(frame)
dst = cv2.drawContours(frame, squares, -1, (0, 255, 0), 3 )
dst_cor = transformation(frame_2, squares)
# cv2.imwrite('transformation.png',dst)

plt.subplot(121),plt.imshow(dst),plt.title('Input')
plt.subplot(122),plt.imshow(dst_cor),plt.title('Output')
plt.show()

# for filename in os.listdir(filepath):
# 	dst_filename = os.path.join(dstpath, filename)
# 	filename = os.path.join(filepath, filename)

# 	print dst_filename
# 	frame = cv2.imread(filename)
# 	squares = find_squares(frame)
# 	dst = transformation(frame, squares)


# 	cv2.imwrite(dst_filename, dst)
