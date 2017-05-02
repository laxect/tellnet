#!/bin/python
import time
import socket
try:
    import my_config as config
except ImportError:
    import cli_config as config

import threading
from message_pack.message_pack import message

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def send_fun():
    while True:
        comment = input()
        me = message(
            recv_from=None, send_to=None, content=comment,
            timestamp=time.ctime(), user_agent=config.user_agent,
            memetype='Text')
        if(comment[0] == '\\'):
            me['memetype'] = 'command'
        s.send(me.package().encode('utf-8'))
        if(comment == '\\exit'):
            s.close()
            exit()


def receiver_fun():
    me = message()
    while True:
        bufff = s.recv(1024000)
        me.unpackage(bufff.decode('utf-8'))
        if me['memetype'] != 'Text':
            print('You have receive a sms that this program don\'t support.')
            continue
        print(
            me['recv_from_name'], ' @ ', me['timestamp'], ' :\n', me.content())
        # print(bufff.decode('utf-8'))


def main():
    s.connect((config.service_addr, config.service_port))
    print('Link Start.\nType \'\help\' for more information')
    sender = threading.Thread(target=send_fun)
    receiver = threading.Thread(target=receiver_fun, daemon=True)
    sender.start()
    receiver.start()


if __name__ == '__main__':
    main()
