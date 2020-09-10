import random
from time import sleep


def rand_wait_min(a=None, b=None):
    a = a if not a else a * 60
    b = b if not b else b * 60
    rand_wait_sec(a, b)


def rand_wait_sec(min_v=2, max_v=3):
    sleep(random.randint(min_v, max_v))
