#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import datetime
import socket
import pickle
import sys
import signal
import struct
import threading
import time
import cv2
import numpy as np

MAX_BYTES = 65535
mcast_group_ip = '239.0.0.1'
mcast_group_port = 10000
object_list = []
running_flag = True
thread_lock = threading.Lock()
color = ['white', 'red', 'blue', 'green', 'yellow']

def quit(signum, frame):
    global running_flag
    print('exit')
    running_flag = False
    sys.exit()

def server(ipaddr, port):
    global object_list
    # 建立端口,设定ip传输协议以及端口协议
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 绑定指定的ip与端口
    sock.bind(('0.0.0.0', port))
    sock.settimeout(3)
    print('Listening at {}'.format(sock.getsockname()))
    # 加入组播组
    # mreq = struct.pack("=4sl", socket.inet_aton(ipaddr), socket.INADDR_ANY)
    # sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while running_flag:
        # 接收信息
        try:
            data, address = sock.recvfrom(MAX_BYTES)
            # 解码
            text = pickle.loads(data)
            thread_lock.acquire()
            object_list = text
            thread_lock.release()
            print('The client at {} send data: {!r}'.format(address, text))
        except socket.timeout:
            object_list = []
            print(datetime.datetime.now())
            pass

def open_video(source):
    print('open source ', source)
    cap = cv2.VideoCapture(source)
    num=0
    while cap.isOpened():
        global running_flag, object_list
        ret, frame = cap.read()
        num = num+1
        if num%3 != 0:
            continue
        frame_height = cap.get(3)
        frame_width = cap.get(4)
        thread_lock.acquire()
        object_list_tmp = object_list
        thread_lock.release()
        for object in object_list_tmp:
            print(object)
            frame = cv2.rectangle(frame, (object[1], object[2]), (object[3], object[4]), (0, 0, 255), 3)
            cv2.putText(frame, color[object[0]], (object[1], object[2]-6), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        frame = cv2.resize(frame, (960, 480))
        cv2.imshow('image', frame)
        k = cv2.waitKey(30)
        if k & 0xff == ord('q'):
            running_flag = False
            break

if __name__ == '__main__':
    thread_recv = threading.Thread(target=server, args=(mcast_group_ip, mcast_group_port))
    thread_recv.start()
    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)
    print('00000000000')
    open_video('rtsp://admin:xl123456@10.0.0.52:554/h264/ch1/sub/av_stream')
    # open_video(r'F:\share\video\qd3\light-detect\rail-car-night-run.mp4')