import numpy as np
import cv2

cap = cv2.VideoCapture("rtsp://admin:waycom12345@172.16.41.1:554/h264/ch1/sub/av_stream")

fourcc = cv2.VideoWriter_fourcc(*'H264')

out = cv2.VideoWriter('testwrite.avi', fourcc, 20.0, (1920, 1080), True)

while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:

        cv2.imshow('frame', frame)
        ret = out.write(frame)
        print(ret)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()