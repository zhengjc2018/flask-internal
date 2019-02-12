from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.contrib.securecookie import SecureCookie
from ico import HTML_TEMPLATE

# 参考：
# http://werkzeug.pocoo.org/docs/contrib/securecookie/


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

    def dispatch_request(self, environ):
        """
        url_map:Map([<Rule '/favicon.ico' (HEAD, GET) -> favicon>,
                     <Rule '/hello/<user>' (HEAD, GET) -> hello>])
        endpoint:hello ,
        values:{'user': 'zjc'}
        """
        url_adapter = self.url_map.bind_to_environ(environ)
        endpoint, values = url_adapter.match()
        print('endpoint:%s, values:%s' % (endpoint, values))
        return self.view_functions[endpoint](**values)

    def route(self, rule, **options):
        def decorator(f):
            endpoint = options.setdefault('endpoint', f.__name__)
            self.url_map.add(Rule(rule, **options))
            self.view_functions[endpoint] = f
            return f
        return decorator

    def open_session(self, request):
        '''
        load_cookie:
        data = request.cookies.get(key)
        if not data:
            return cls(secret_key=secret_key)
        return cls.unserialize(data, secret_key)
        '''
        return SecureCookie.load_cookie(request,
                                        key=self.session_cookie_name,
                                        secret_key=self.secret_key)

    def save_session(self, session, response):
        session.save_cookie(response, key=self.session_cookie_name)

    def make_response(self, session, response):
        self.save_session(session, response)
        return response

    def wsgi_app(self, environ, start_response):
        request = self.request_class(environ)

        session = self.open_session(request)
        print('total_request: %d' % session.setdefault('total_request', 0))
        session['total_request'] += 1

        rv = self.dispatch_request(environ)
        response = self.response_class(rv)
        response = self.make_response(session, response)
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
        return HTML_TEMPLATE
        # return '🙈'

    @app.route('/hello/<user>', methods=['GET'], endpoint='he')
    def hello(user):
        # session 对象需要通过参数透传到这里才能使用 :(
        return 'hello %s' % user

    app.run('0.0.0.0', 5000, debug=True)
