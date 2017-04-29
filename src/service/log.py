import time
import sys


class log:
    def __init__(self, log_file_name='log_file'):
        self.log_file = open("log_file.log", "a")
        self.log_file.seek(2)

    def __del__(self):
        self.log_file.close()

    def new_log(self, comment):
        self.log_file.write(comment + "==============\n" + time.ctime() + '\n')


def main():
    lg = log()
    lg.new_log('aaaa\nbbbb')
    sys.exit()
    lg.new_log(input())


if __name__ == '__main__':
    main()
