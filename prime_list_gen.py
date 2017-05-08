# !/bin/usr/python3


def prime_gen():
    re = []
    a = [True]*6000

    for i in range(2, 6000):
        if a[i]:
            re.append(i)
            for j in range(2, 6000//i):
                a[i*j] = False
    return re
