import time
import threading
import functools


class log:
    def __init__(self, log_file_name='log_file'):
        self.log_file = open("log_file.log", "a")
        self.lock = threading.Lock()

    def __del__(self):
        self.log_file.close()

    def new_log(self, comment):
        self.lock.acquire()
        nl = (comment + "\nthis log added at " + time.ctime() + '\n')
        print(nl)
        self.log_file.write(nl+'\n')
        self.log_file.flush()
        self.lock.release()

    def log_thread(self):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kw):
                self.new_log('[Th:new Thread]\n %s' % threading.currentThread())
                re = func(*args, **kw)
                self.new_log(
                    '[Th:Thread close]\n %s' % threading.currentThread())
                return re
            return wrapper
        return decorator


def main():
    lg = log()
    lg.new_log('aaaa\nbbbb')
    del lg


if __name__ == '__main__':
    main()
