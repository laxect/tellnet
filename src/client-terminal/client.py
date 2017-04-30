#!/bin/python
import time
import socket
try:
    import my_config as config
except ImportError:
    import config

import threading
from message_pack import message

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def send_fun():
    while True:
        comment = input()
        if len(comment) > 500:
            print('Error : Too long content to send.\n')
            continue
        if comment:
            me = message(None, None, comment, time.ctime(), config.user_agent)
            s.send(me.package().encode('utf-8'))
        if(comment == '\\exit'):
            s.close()
            exit()


def receiver_fun():
    me = message()
    while True:
        bufff = s.recv(1024)
        if bufff:
            me.unpackage(bufff.decode('utf-8'))
        else:
            break
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
