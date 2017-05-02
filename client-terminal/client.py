#!/bin/python
import time
import socket
try:
    import my_config as config
except ImportError:
    import config

import threading
from message_pack import message, message_pack

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def send_fun():
    while True:
        comment = input()
        if comment:
            mp = message_pack(
                recv_from=None, send_to=None, content=comment,
                timestamp=time.ctime(), user_agent=config.user_agent,
                memetype='Text')
            for me in mp:
                s.send(me.package().encode('utf-8'))
        if(comment == '\\exit'):
            s.close()
            exit()


def receiver_fun():
    me = message()
    tmp = message()
    while True:
        bufff = s.recv(10240)
        tmp.unpackage(bufff.decode('utf-8'))
        if tmp['pack_num'] == 0:
            me = tmp
        elif tmp['pack_num'] == 1:
            me = tmp
            continue
        else:
            me.content_join(tmp['content'])
            if tmp['pack_num'] > 1:
                continue
        print(
            me['recv_from_name'], ' @ ', me['timestamp'], ' :\n', me.content())
        # print(bufff.decode('utf-8'))


def main():
    # print('socket builded, please input the addr of service.')
    # service_addr = input()
    # if (service_addr == ''):
    #    service_addr = '127.0.0.1'
    s.connect((config.service_addr, config.service_port))
    print('Link Start.\nType \'\help\' for more information')
    sender = threading.Thread(target=send_fun)
    receiver = threading.Thread(target=receiver_fun, daemon=True)
    sender.start()
    receiver.start()


if __name__ == '__main__':
    main()
