import cv2

# cap = cv2.VideoCapture('F:\\share\\video\\01.avi')
cap = cv2.VideoCapture('rtsp://admin:waycom12345@172.16.41.203:554/cam/realmonitor?channel=1&subtype=1')
while cap.isOpened():
    ret, frame = cap.read()
    cv2.imshow('image', frame)
    k = cv2.waitKey(20)
    if k & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
