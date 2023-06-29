import cv2
import numpy as np
import copy
import os

input_file = r'F:\share\video\cd1-video\5-20200916-080_person_output_02.avi'
output_file = os.path.splitext(input_file)[0] + '-add_polylines' + os.path.splitext(input_file)[1]
cap = cv2.VideoCapture(input_file)
fps = cap.get(cv2.CAP_PROP_FPS)
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
videoWriter = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'XVID'), fps, size)


while cap.isOpened():
    ret, frame = cap.read()
    frame_copy = copy.deepcopy(frame)

    pts1 = np.array([[1085, 147], [1280, 235], [1246, 600], [1111, 720], [1035, 580]], np.int32)
    cv2.polylines(frame, [pts1], True, (0, 255, 255), 1)
    cv2.fillPoly(frame, [pts1], (110, 250, 160))

    pts2 = np.array([[0, 209], [236, 142], [269, 603], [143, 720], [0, 690]], np.int32)
    cv2.polylines(frame, [pts2], True, (0, 255, 255), 1)
    cv2.fillPoly(frame, [pts2], (110, 250, 160))

    frame_out = cv2.addWeighted(frame, 0.3, frame_copy, 0.7, 5)
    videoWriter.write(frame_out)
    # cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow('image', 0, 0)
    cv2.imshow('image', frame_out)

    k = cv2.waitKey(20)
    if k & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
