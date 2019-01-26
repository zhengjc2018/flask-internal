import threading
import time

# 参考：
# https://docs.python.org/3/library/threading.html#thread-local-data
request = threading.local()


def run(payload, seconds):
    request.payload = payload
    time.sleep(seconds)
    print('%s %s' % (threading.current_thread().name, request.payload))


request.payload = 'change to foo'
t1 = threading.Thread(target=run, args=('change to hello', 3))
t2 = threading.Thread(target=run, args=('change to world', 1))
t1.start()
t2.start()
t1.join()
t2.join()
print('%s %s' % (threading.current_thread().name, request.payload))
