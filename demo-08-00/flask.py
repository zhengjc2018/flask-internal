from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.contrib.securecookie import SecureCookie
from werkzeug.local import LocalStack, LocalProxy

_request_ctx_stack = LocalStack()
current_app = LocalProxy(lambda: _request_ctx_stack.top.app)
request = LocalProxy(lambda: _request_ctx_stack.top.request)
session = LocalProxy(lambda: _request_ctx_stack.top.session)


class _RequestContext(object):
    def __init__(self, app, environ):
        self.app = app
        self.request = app.request_class(environ)
        self.session = app.open_session(self.request)
        self.url_adapter = app.url_map.bind_to_environ(environ)

    def __enter__(self):
        _request_ctx_stack.push(self)

    def __exit__(self, exc_type, exc_value, tb):
        _request_ctx_stack.pop()


class FlaskRequest(Request):
    pass


class FlaskResponse(Response):
    default_mimetype = 'text/html'


class Flask(object):
    request_class = FlaskRequest
    response_class = FlaskResponse

    secret_key = 'dangerous'
    session_cookie_name = 'flask_session'

    def __init__(self):
        self.debug = False
        self.url_map = Map()
        self.view_functions = {}

    def dispatch_request(self):
        endpoint, values = _request_ctx_stack.top.url_adapter.match()
        return self.view_functions[endpoint](**values)

    def route(self, rule, **options):
        def decorator(f):
            endpoint = options.setdefault('endpoint', f.__name__)
            self.url_map.add(Rule(rule, **options))
            self.view_functions[endpoint] = f
            return f
        return decorator

    def open_session(self, request):
        return SecureCookie.load_cookie(request,
                                        key=self.session_cookie_name,
                                        secret_key=self.secret_key)

    def save_session(self, response):
        session.save_cookie(response, key=self.session_cookie_name)

    def make_response(self, response):
        self.save_session(response)
        return response

    def request_context(self, environ):
        return _RequestContext(self, environ)

    def test_request_context(self, *args, **kwargs):
        from werkzeug.test import create_environ
        return self.request_context(create_environ(*args, **kwargs))

    def test_client(self):
        from werkzeug.test import Client
        return Client(self, self.response_class, use_cookies=True)

    def wsgi_app(self, environ, start_response):
        with self.request_context(environ):
            print('user: %s' % session.setdefault('user', 'none'))
            print('total_request: %d' % session.setdefault('total_request', 0))
            session['total_request'] += 1

            rv = self.dispatch_request()
            response = self.response_class(rv)
            response = self.make_response(response)
            return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def run(self, host='localhost', port=5000, **options):
        if 'debug' in options:
            self.debug = options.pop('debug')

        options.setdefault('use_reloader', self.debug)
        options.setdefault('use_debugger', self.debug)

        from werkzeug.serving import run_simple
        run_simple(host, port, self, **options)


if __name__ == '__main__':
    app = Flask()

    @app.route('/favicon.ico', methods=['GET'])
    def favicon():
        return '🙈'

    @app.route('/hello/<user>', methods=['GET'])
    def hello(user):
        session['user'] = user
        return 'hello %s' % user

    # 参考：
    # http://werkzeug.pocoo.org/docs/test/
    client = app.test_client()
    assert client.get('/hello/bar').data == b'hello bar'

    with app.test_request_context('/name/foo'):
        assert hello('foo') == 'hello foo'
        assert session['user'] == 'foo'
