class ConfigAttribute(object):
    def __init__(self, name):
        self.__name__ = name

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        rv = obj.config[self.__name__]
        return rv

    def __set__(self, obj, value):
        obj.config[self.__name__] = value


class App(object):
    secret_key = ConfigAttribute('SECRET_KEY')

    def __init__(self, config):
        self.config = config


old_config = {'SECRET_KEY': 'default key'}
app = App(old_config)
print(app.secret_key)

app.config = {'SECRET_KEY': 'new secret key'}
print(app.secret_key)
