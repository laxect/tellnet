#!/bin/python
# sys module
import sys
import time
import socket
import threading
# my module
import log
import __help__
from message_pack import message
# from message_struct import message
from user_struct import user_pool
from tunel_struct import tunel_pool
import config


message_cnt = 0
users = user_pool()
tunels = tunel_pool()
public_buffer = dict()
buffer_lock = threading.Lock()
lg = log.log(log_file_name='log_file')


def command_fun(comment, user_id):
    re = ''
    if not users.user_con(user_id):
        re = 'Error : No such user or admin.'
        return message(
            0, user_id, re, time.ctime(), config.service_agent, 'Admin')
    this_user = users.pool[user_id]
    if comment == '\\help':
        re = __help__.str_help
    elif comment == '\\tn':
        re = 'you are now in ' + tunels.pool[this_user.tunel].name
    elif comment[0:9] == '\\chtnname':
        if tunels.chname_tn(this_user.tunel, comment[10:]):
            re = (
                'the tunel\'s name change to ' +
                tunels.pool[this_user.tunel].name)
        else:
            re = 'you can\'t change name of this tunel'
    elif comment[0:5] == '\\chtn':
        tunel_to = comment[6:]
        tunels.join_tn('t'+tunel_to)
        users.user_chtn(user_id, 't'+tunel_to)
        re = 'you are now in ' + tunels.pool[this_user.tunel].name
    elif comment[0:7] == '\\chname':
        users.user_chname(user_id, comment[8:])
        re = 'your name change to ' + this_user.name
    else:
        re = (
            'there is no command like ' +
            comment+'\n' +
            'type \\help for more information')
    return message(0, user_id, re, time.ctime(), config.service_agent, 'Admin')


@lg.log_thread()
def recv_fun(sock, user_id):
    global message_cnt
    while users.user_con(user_id):
        this_user = users.pool[user_id]
        me = message()
        data = sock.recv(config.buff_size)
        if not data:
            users.user_logout(user_id)
            exit()
        if not me.unpackage(data.decode('utf-8')) or me.content() == '\\exit':
            users.user_logout(user_id)
            exit()
        # to prevent user cheat
        me['recv_from'] = this_user.num
        me['send_to'] = this_user.tunel
        me['recv_from_name'] = this_user.name
        # end of above
        buffer_lock.acquire()
        # comment = data.decode('utf-8')
        if me.content()[0] == '\\':
            message_cnt += 1
            public_buffer[message_cnt] = [
                command_fun(me.content(), this_user.num), users.user_cnt]
        else:
            message_cnt += 1
            public_buffer[message_cnt] = [me, users.user_cnt]
        buffer_lock.release()


@lg.log_thread()
def send_fun(sock, user_id):
    global messgae_cnt
    local_message_cnt = message_cnt
    while users.user_con(user_id):
        this_user = users.pool[user_id]
        buffer_lock.acquire()
        if (local_message_cnt < message_cnt):
            local_message_cnt += 1
            me = public_buffer[local_message_cnt][0]
            if (me.recv_from() != user_id and (
                    me.send_to() == this_user.tunel
                    or me.send_to() == user_id)):
                sock.send(
                    me.package().encode('utf-8')
                    )
                public_buffer[local_message_cnt][1] -= 1
        buffer_lock.release()


@lg.log_thread()
def public_control():
    global message_cnt
    local_clear_cnt = 0
    while True:
        buffer_lock.acquire()
        if local_clear_cnt not in public_buffer:
            if local_clear_cnt < message_cnt:
                local_clear_cnt += 1
        elif local_clear_cnt < message_cnt:
            if public_buffer[local_clear_cnt][1] == 0:
                public_buffer.pop(local_clear_cnt)
                local_clear_cnt += 1
        buffer_lock.release()


@lg.log_thread()
def tcplink(sock, addr, user_id, lg=lg):
    # global lg
    lg.new_log('[U:new user log in] %s:%s ' % addr)
    th_r = threading.Thread(target=recv_fun, args=(sock, user_id), daemon=True)
    th_s = threading.Thread(target=send_fun, args=(sock, user_id), daemon=True)
    th_s.start()
    th_r.start()
    th_r.join()
    users.user_logout(user_id)
    lg.new_log('[U:user log out] %s:%s ' % addr)


@lg.log_thread()
def link_control(s):
    # global lg
    # lg.new_log('[Th : thread create]\n%s' % threading.currentThread())
    s.bind(('0.0.0.0', config.service_port))
    s.listen(20)
    # print('wait for ......')
    while True:
        sock, addr = s.accept()
        threading.Thread(
           target=tcplink, args=(sock, addr, users.user_login()), daemon=True
        ).start()


def main():
    global lg
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    threading.Thread(target=public_control, args=(), daemon=True).start()
    threading.Thread(target=link_control, args=(s, ), daemon=True).start()
    while True:
        comment = input()
        if comment == 'exit':
            break
    del lg
    s.close()
    sys.exit()


if __name__ == '__main__':
    main()
