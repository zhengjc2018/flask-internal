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
    session_cookie_name = ConfigAttribute('SESSION_COOKIE_NAME')

    def __init__(self, config):
        self.config = config

    def update_config(self, config):
        self.config.update(config)


old_config = {
    'SECRET_KEY': 'hello world',
    'SESSION_COOKIE_NAME': 'app_session'
}
app = App(old_config)
print(app.secret_key)
print(app.session_cookie_name)

new_config = {
    'SECRET_KEY': 'hello new world',
    'SESSION_COOKIE_NAME': 'new_app_session'
}
app.update_config(new_config)
print(app.secret_key)
print(app.session_cookie_name)
