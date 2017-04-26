import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def send_fun():
    while True:
        comment = input()
        s.send(comment.encode('utf-8'))
        if(comment == 'exit'):
            s.close()
            exit()


def receiver_fun():
    buff = []
    while True:
        bufff = s.recv(1024)
        if bufff:
            buff.append(bufff)
        else:
            break
        print(bufff.decode('utf-8'))


def main():
    print('socket builded, please input the addr of service.')
    service_addr = input()
    if (service_addr == ''):
        service_addr = '127.0.0.1'
    s.connect((service_addr, 2048))
    print('Link Start.\nType \'exit\' to leave')
    sender = threading.Thread(target=send_fun)
    receiver = threading.Thread(target=receiver_fun, daemon=True)
    sender.start()
    receiver.start()


if __name__ == '__main__':
    main()
