import cv2

x1, y1, x2, y2 = 0, 0, 100, 100
video = cv2.VideoCapture(r"F:\share\video\01.avi")
#将视频文件初始化为VideoCapture对象
fps = video.get(cv2.CAP_PROP_FPS)
size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print(video.get(cv2.CAP_PROP_FPS))# 返回帧率
print(video.get(cv2.CAP_PROP_FRAME_WIDTH))
print(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
video_writer = cv2.VideoWriter('outputVideo.avi', cv2.VideoWriter_fourcc(*'XVID'), fps, size)

success, frame = video.read()

#read()方法读取视频下一帧到frame，当读取不到内容时返回false!
while success and cv2.waitKey(1) & 0xFF != ord('q'):
#等待1毫秒读取键键盘输入，最后一个字节是键盘的ASCII码。ord()返回字母的ASCII码
    cv2.rectangle(frame, (x1, y1), (y2, y2), (0, 255, 0), 3)
    cv2.putText(frame, "name", (x2,y2), cv2.FONT_HERSHEY_COMPLEX_SMALL,0.8, (255, 0, 0))
    cv2.imshow('frame', frame)
    success, frame = video.read()
    video_writer.write(frame)
cv2.destroyAllWindows()
video.release()
video_writer.release()