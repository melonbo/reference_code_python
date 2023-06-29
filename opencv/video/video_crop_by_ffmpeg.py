import os
import cv2

#ffmpeg -ss 00:01:00 -i video.mp4 -to 00:02:00 -c copy -copyts cut.mp4

path = r'F:\share\video\cd1-video\CD1-105-05-20200916-080000.ts'
path_to = r'F:\share\video\cd1-video'
fpath, fname = os.path.split(path)
source_video_file = '"' + path + '"'
output_video_file = '"' + os.path.join(path_to, fname) + '"'
start_hour, start_min, start_sec = 0, 56, 20
stop_hour, stop_min, stop_sec = 0, 56, 50

start_time = str(start_hour) + ':' + str(start_min) + ':' + str(start_sec)
stop_time = str(stop_hour) + ':' + str(stop_min) + ':' + str(stop_sec)

cmd = 'ffmpeg' + ' -i ' + source_video_file + ' -ss ' + start_time + ' -to ' + stop_time + ' -c copy ' + output_video_file + ' -y'
print(cmd)
os.system(cmd)