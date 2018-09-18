from contextlib import contextmanager
import time

@contextmanager
def timer(func):
    try:
        start = time.time()
        yield func()
    finally:
        end = time.time()
        print(end-start)


def func():
    for i in range(9999999):
        pass
    time.sleep(1)

with timer(func) as timer:
    pass