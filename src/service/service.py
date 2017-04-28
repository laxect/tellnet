#!/bin/python
import socket
import threading
import __help__
from message_struct import message
from user_struct import user

cnt = 0
message_cnt = 0
buff_size = 1024
public_buffer = dict()
buffer_lock = threading.Lock()
tunels = dict()
tunels['t0'] = 'main tunel'


def command_fun(comment, client):
    if comment == '\\help':
        return 'Admin :\n'+__help__.str_help
    elif comment == '\\tn':
        return 'Admin : you are now in ' + tunels[client.tunel]
    elif comment[0:5] == '\\chtn':
        tunel_to = comment[6:]
        client.tunel = tunel_to
        return 'Admin : you are now in ' + tunels.setdefault(tunel_to, 'Ans')
    else:
        return (
            'Admin : there is no command like ' +
            comment+'\n' +
            'type \\help for more information'
        )


def recv_fun(sock, client):
    global message_cnt
    global cnt
    while True:
        data = sock.recv(buff_size)
        if not data or data.decode('utf-8') == '\\exit':
            message_cnt += 1
            public_buffer[message_cnt] = message(
                0, client.num, '\\exit', 1
            )
            exit()
        buffer_lock.acquire()
        comment = data.decode('utf-8')
        if comment[0] == '\\':
            message_cnt += 1
            public_buffer[message_cnt] = message(
                0, client.num, command_fun(comment, client), 1
            )
        else:
            message_cnt += 1
            public_buffer[message_cnt] = message(
                client.num, client.tunel, client.name+' :'+comment, cnt
            )
        buffer_lock.release()


def send_fun(sock, client):
    global messgae_cnt
    global cnt
    local_message_cnt = message_cnt
    while True:
        buffer_lock.acquire()
        if (local_message_cnt < message_cnt):
            local_message_cnt += 1
            if (
                public_buffer[local_message_cnt].se != client.num and
                (
                    public_buffer[local_message_cnt].re == client.tunel
                    or public_buffer[local_message_cnt].re == client.num
                )
            ):
                sock.send(
                    public_buffer[local_message_cnt].comment.encode('utf-8')
                )
                public_buffer[local_message_cnt].cnt -= 1
        buffer_lock.release()


def public_control():
    global message_cnt
    local_clear_cnt = 0
    while True:
        buffer_lock.acquire()
        if local_clear_cnt not in public_buffer:
            if local_clear_cnt < message_cnt:
                local_clear_cnt += 1
        elif local_clear_cnt < message_cnt:
            if public_buffer[local_clear_cnt].cnt == 0:
                public_buffer.pop(local_clear_cnt)
                local_clear_cnt += 1
        buffer_lock.release()


def tcplink(sock, addr, client):
    global cnt
    cnt += 1
    print('Accept new connection from %s:%s...' % addr)
    th = threading.Thread(target=recv_fun, args=(sock, client))
    threading.Thread(target=send_fun, args=(sock, client), daemon=True).start()
    th.start()
    th.join()
    cnt -= 1
    print('Connection from %s:%s closed.' % addr)


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 2048))
    s.listen(20)
    print('wait for ......')
    threading.Thread(target=public_control, args=(), daemon=True).start()
    while True:
        sock, addr = s.accept()
        threading.Thread(
            target=tcplink, args=(sock, addr, user(cnt+1, 't0'))
        ).start()


if __name__ == '__main__':
    main()
