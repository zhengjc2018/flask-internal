class Proxy(object):
    def __init__(self, local, name=None):
        object.__setattr__(self, '_Proxy__local', local)
        object.__setattr__(self, '__name__', name)

    def _get_current_object(self):
        if callable(self.__local):
            return self.__local()
        try:
            return getattr(self.__local, self.__name__)
        except AttributeError:
            raise RuntimeError('no object bound to %s' % self.__name__)

    def __getattr__(self, name):
        return getattr(self._get_current_object(), name)

    def __setattr__(self, name, value):
        setattr(self._get_current_object(), name, value)

    def __delattr__(self, name):
        delattr(self._get_current_object(), name)


class User(object):
    def __init__(self, name):
        self.name = name
        self.langs = []


class Stack(object):
    def __init__(self):
        self._list = []

    def push(self, obj):
        self._list.append(obj)

    def pop(self):
        self._list.pop()

    @property
    def top(self):
        if len(self._list) > 0:
            return self._list[len(self._list)-1]
        else:
            return None


user = User('foo')
langs = Proxy(user, 'langs')
langs.append('en')
langs.append('cn')
print(user.langs)

users = Stack()
user_foo = User('foo')
user_foo.langs.append('cn')
users.push(user_foo)
user_bar = User('bar')
user_bar.langs.append('en')
users.push(user_bar)
current_user = Proxy(lambda: users.top)
print(current_user.name, current_user.langs)
users.pop()
print(current_user.name, current_user.langs)
