import threading
import time

request = threading.local()


def run(name, seconds):
    request.name = name
    time.sleep(seconds)
    print('%s %s' % (threading.current_thread().name, request.name))


request.name = 'foo'
t1 = threading.Thread(target=run, args=('hello', 3))
t2 = threading.Thread(target=run, args=('world', 1))
t1.start()
t2.start()
t1.join()
t2.join()
print('%s %s' % (threading.current_thread().name, request.name))
