#!/bin/python
import socket
import threading
import __help__
from message_struct import message
from user_struct import user_pool
from tunel_struct import tunel_pool

message_cnt = 0
buff_size = 1024
public_buffer = dict()
buffer_lock = threading.Lock()
tunels = tunel_pool()
users = user_pool()


def command_fun(comment, user_id):
    if not users.user_con(user_id):
        return 'Error : No such user or admin.'
    this_user = users.pool[user_id]
    if comment == '\\help':
        return 'Admin :\n'+__help__.str_help
    elif comment == '\\tn':
        return 'Admin : you are now in ' + tunels.pool[this_user.tunel].name[1:]
    elif comment[0:9] == '\\chtnname':
        if tunels.chname_tn(this_user.tunel, comment[10:]):
            return(
                'the tunel\'s name change to ' +
                tunels.pool[this_user.tunel].name)
        else:
            return 'you can\'t change name of this tunel'
    elif comment[0:5] == '\\chtn':
        tunel_to = comment[6:]
        tunels.join_tn('t'+tunel_to)
        users.user_chtn(user_id, 't'+tunel_to)
        return 'Admin : you are now in ' + tunels.pool[this_user.tunel].name[1:]
    elif comment[0:7] == '\\chname':
        users.user_chname(user_id, comment[8:])
        return 'Admin : your name change to ' + this_user.name
    else:
        return (
            'Admin : there is no command like ' +
            comment+'\n' +
            'type \\help for more information')


def recv_fun(sock, user_id):
    global message_cnt
    while users.user_con(user_id):
        this_user = users.pool[user_id]
        data = sock.recv(buff_size)
        if not data or data.decode('utf-8') == '\\exit':
            message_cnt += 1
            public_buffer[message_cnt] = message(
                0, user_id, '\\exit', 1)
            users.user_logout(user_id)
            exit()
        buffer_lock.acquire()
        comment = data.decode('utf-8')
        if comment[0] == '\\':
            message_cnt += 1
            public_buffer[message_cnt] = message(
                0, user_id, command_fun(comment, user_id), 1)
        else:
            message_cnt += 1
            public_buffer[message_cnt] = message(
                user_id, this_user.tunel, this_user.name+' :'+comment,
                users.user_cnt)
        buffer_lock.release()


def send_fun(sock, user_id):
    global messgae_cnt
    local_message_cnt = message_cnt
    while users.user_con(user_id):
        this_user = users.pool[user_id]
        buffer_lock.acquire()
        if (local_message_cnt < message_cnt):
            local_message_cnt += 1
            if (public_buffer[local_message_cnt].se != user_id and (
                    public_buffer[local_message_cnt].re == this_user.tunel
                    or public_buffer[local_message_cnt].re == user_id)):
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


def tcplink(sock, addr, user_id):
    print('Accept new connection from %s:%s...' % addr)
    th = threading.Thread(target=recv_fun, args=(sock, user_id))
    threading.Thread(target=send_fun, args=(sock, user_id)).start()
    th.start()
    th.join()
    users.user_logout(user_id)
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
            target=tcplink, args=(sock, addr, users.user_login())
        ).start()


if __name__ == '__main__':
    main()
