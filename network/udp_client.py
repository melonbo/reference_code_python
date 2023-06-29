#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import socket
import pickle
from datetime import datetime

MAX_BYTES = 65535

def client(port, data):
    # 建立端口
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # sock.bind(("127.0.0.1",5555))
    text = 'The time is {}'.format(datetime.now())

    print(text)
    data = pickle.dumps(data)

    # 发送消息
    sock.sendto(data, ('127.0.0.1', port))
    print('The OS assigned me the address {}'.format(sock.getsockname()))

    data, address = sock.recvfrom(MAX_BYTES) # Danger! See Chapter 2
    text = data.decode('ascii')
    print('The server {} replied {!r}'.format(address, text))

if __name__ == '__main__':
    for i in [range(5), list('abc'), dict(a=1,b=2)]:
        client(1060, i)
