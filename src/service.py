import socket
import threading
import time

cnt = 0
message_cnt = 0
buff_size = 1024
public_buffer = dict()
buffer_lock = threading.Lock()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 2048))
s.listen(20)
print('wait for ......')

def recv_fun(sock, num):
  global message_cnt
  global cnt
  while True:
    data = sock.recv(buff_size)
    if not data or data.decode('utf-8') == 'exit':
      exit()
    buffer_lock.acquire()
    message_cnt += 1
    public_buffer[message_cnt] = [data.decode('utf-8'), cnt, num]
    buffer_lock.release()

def send_fun(sock, num):
  global messgae_cnt
  global cnt
  local_message_cnt = message_cnt
  while True:
    buffer_lock.acquire()
    if (local_message_cnt < message_cnt):
      local_message_cnt += 1
      if (public_buffer[2] != num):
        sock.send(public_buffer[local_message_cnt][0].encode('utf-8'))
        public_buffer[local_message_cnt][1] -= 1
    buffer_lock.release()
    
def public_control():
  global message_cnt
  local_clear_cnt = 0
  while True:
    if not local_clear_cnt in public_buffer and local_clear_cnt <= message_cnt:
      local_clear_cnt += 1
    if (local_clear_cnt < message_cnt and public_buffer[local_clear_cnt][1] == 0):
      public_buffer.pop(local_clear_cnt)
      local_clear_cnt += 1
      
  
def tcplink(sock, addr, num):
  global cnt
  cnt += 1
  print('Accept new connection from %s:%s...' % addr)
  threading.Thread(target=recv_fun, args=(sock, num), daemon=True).start()
  th = threading.Thread(target=send_fun, args=(sock, num))
  th.start()
  th.join()
  cnt -= 1
  print('Connection from %s:%s closed.' % addr)
  

threading.Thread(target=public_control, args=()).start()
while True:
  sock, addr = s.accept()
  threading.Thread(target=tcplink, args=(sock, addr, cnt)).start()
