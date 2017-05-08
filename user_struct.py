#!/bin/python3


class user:
    def __init__(self, num, tunel='t0', name='unknown'):
        self.num = num
        self.tunel = tunel
        self.name = name


class user_pool:
    def __init__(self):
        self.pool = {}
        self.pool[0] = user(num=0, tunel='t0', name='Admin')
        self.user_cnt = 0
        self.cnt = 1

    def user_login(self):
        self.pool[self.cnt] = user(num=self.cnt, tunel='t0', name='unknown')
        self.cnt += 1
        self.user_cnt += 1
        return self.cnt-1

    def user_con(self, user_id):
        return user_id in self.pool

    def user_chname(self, user_id, new_name):
        if self.user_con(user_id):
            self.pool[user_id].name = new_name
        return new_name

    def user_logout(self, user_id):
        if self.user_con(user_id):
            self.pool.pop(user_id)
            self.user_cnt -= 1

    def user_chtn(self, user_id, tn_real_id):
        self.user_join_tn(user_id, tn_real_id)
        self.user_leave_tn(user_id, tn_real_id)

    def user_join_tn(self, user_id, tn_real_id):
        'user join a new tunel'
        if self.user_con(user_id):
            self.pool[user_id].tunel *= tn_real_id

    def user_leave_tn(self, user_id, tn_real_id):
        'leave a tunel'
        if self.user_con(user_id) and not self.pool[user_id].tunel % tn_real_id:
            self.pool[user_id].tunel //= tn_real_id


def main():
    test_u = user(0)
    del test_u


if __name__ == '__main__':
    main()
