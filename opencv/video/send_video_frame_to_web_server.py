import cv2
import numpy as np
import websocket
import threading

import cv2
print(cv2.VideoWriter_fourcc('M','J','P','G'))
print(cv2.VideoWriter_fourcc('M','P','4','2'))
print(cv2.VideoWriter_fourcc('A','V','C','1'))

# RTSP视频流地址
rtsp_url = "rtsp://admin:waycom12345@172.16.41.1:554/h264/ch1/sub/av_stream"

# WebSocket服务器地址
websocket_url = "ws://localhost:8080"

# 视频编码格式
fourcc = cv2.VideoWriter_fourcc(*'H264')
print(fourcc)

# 创建VideoCapture对象
cap = cv2.VideoCapture(rtsp_url)

# 获取视频帧率和分辨率
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(fps, width, height)

# 创建VideoWriter对象，用于将视频帧转换为H.264格式
writer = cv2.VideoWriter("output.mp4", fourcc, fps, (width, height))

# 创建WebSocket连接
ws = websocket.create_connection(websocket_url)

# 定义发送视频帧的函数
def send_frame():
    while True:
        # 读取视频帧
        ret, frame = cap.read()
        if ret:
            # 将视频帧写入VideoWriter对象
            writer.write(frame)
            # 将视频帧转换为二进制数据
            data = cv2.imencode('.mp4', frame)[1].tobytes()
            # 发送视频帧到WebSocket服务器
            ws.send(data)
        else:
            break

# 启动发送视频帧的线程
thread = threading.Thread(target=send_frame)
thread.start()

# 等待线程结束
thread.join()

# 释放资源
cap.release()
writer.release()
ws.close()
