#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import socket
import pickle

MAX_BYTES = 65535

def server(port):
    # 建立端口,设定ip传输协议以及端口协议
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 绑定指定的ip与端口
    sock.bind(('127.0.0.1', port))
    print('Listening at {}'.format(sock.getsockname()))

    while True:
        # 接收信息
        data, address = sock.recvfrom(MAX_BYTES)
        # 解码
        text = pickle.loads(data)
        print('The client at {} says {!r}'.format(address, text))
        text = 'Your data was {} bytes long'.format(len(data))
        data = text.encode('ascii')

        # 发送信息
        sock.sendto(data, address)

if __name__ == '__main__':
    server(1060)
