import time


class log:
    def __init__(self, log_file_name='log_file'):
        self.log_file = open("log_file.log", "w+")

    def __del__(self):
        self.log_file.close()

    def new_log(self, comment):
        self.log_file.write(comment + time.ctime() + '\n')
