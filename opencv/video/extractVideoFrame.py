# coding:utf8
import cv2
import sys
import os

# example python extractVideoFrame.py video 25
frame_num = 0
freq = 1

video_capture = cv2.VideoCapture(sys.argv[1])
video_id = sys.argv[1].split('.')[0]
frames_all = video_capture.get(7)

if not os.path.exists(video_id):
    os.mkdir(video_id)

if len(sys.argv) == 3:
    freq = sys.argv[2]

while True:
    is_successfully_read, im = video_capture.read()
    if not is_successfully_read:
        break
    frame_num += 1
    print("\rframe num %d/%d" % (frame_num, frames_all), end="")
    if frame_num % int(freq) == 0:
        cv2.imwrite(os.path.join(video_id, "%05d"%frame_num+'.jpg'), im)
        # print("image shape=%d"%im.shape)
