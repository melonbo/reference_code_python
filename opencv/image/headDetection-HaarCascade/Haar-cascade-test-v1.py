import cv2
import numpy as np

head_cascade = cv2.CascadeClassifier('cascade.xml')

test_cases = ['test.jpg', 'example.jpg', 'face.jpg']

img = cv2.imread(test_cases[0])

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

heads = head_cascade.detectMultiScale(gray, 1.3, 5)

print(len(heads))

i = 0
for (x,y,w,h) in heads:
	cv2.rectangle(img, (x, y), (x+w, y+h), (255,0,0), 2)
	i = i + 1
	cv2.putText(img, ('head_%03d' % i), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 1, cv2.LINE_AA)

cv2.imshow('img', img)
cv2.waitKey(0)
cv2.imwrite('test-result.jpg', img)
cv2.destroyAllWindows()
