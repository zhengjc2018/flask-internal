from contextlib import contextmanager


class Connection(object):
    def __enter__(self):
        print('connection A open')

    def __exit__(self, exc_type, exc_value, tb):
        print('connection A close')


with Connection():
    print('execute sql with A')


class Database(object):
    @contextmanager
    def connect(self):
        try:
            print('connection B open')
            # object() as a fake connection only for demo
            yield object()
        finally:
            print('connection B close')


db = Database()
with db.connect():
    print('execute sql with B')
