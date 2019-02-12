from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
# from exceptions import MyExceptions, err_handle
from werkzeug.exceptions import HTTPException
# from flask import abort

# 参考：
# http://werkzeug.pocoo.org/docs/routing/#quickstart


class BaseError(HTTPException):
    def __init__(self, code, message):
        self.code = code
        self.message = message.encode('utf-8')

    def show(self):
        return '%s %s' % (self.code, self.message)


class FlaskRequest(Request):
    pass


class FlaskResponse(Response):
    default_mimetype = 'text/html'


class Flask(object):
    request_class = FlaskRequest
    response_class = FlaskResponse

    def __init__(self):
        self.debug = False
        self.url_map = Map()
        self.view_functions = {}

    def dispatch_request(self, environ):
        url_adapter = self.url_map.bind_to_environ(environ)
        endpoint, values = url_adapter.match()
        return self.view_functions[endpoint](**values)

    def route(self, rule, **options):
        def decorator(f):
            endpoint = options.setdefault('endpoint', f.__name__)
            self.url_map.add(Rule(rule, **options))
            self.view_functions[endpoint] = f
            return f
        return decorator

    def wsgi_app(self, environ, start_response):
        try:
            rv = self.dispatch_request(environ)
            response = self.response_class(rv)
            data = response(environ, start_response)
            return data
        except HTTPException as e:
            response = FlaskResponse(e.message, status=e.code)
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

    # @staticmethod
    def errorhandle(self):
        def inner(f):
            message, code = f()
            error = BaseError(code, message)
            return error
        return inner


if __name__ == '__main__':
    app = Flask()

    @app.route('/favicon.ico', methods=['GET'])
    def favicon():
        return '🙈'

    @app.route('/hello/<user>', methods=['GET'])
    def hello(user):
        return 'hello %s' % user

    @app.route('/hello/bye', methods=['GET', 'POST'])
    def gun():
        raise not_404_found

    @app.errorhandle()
    def not_404_found():
        return "NOT FOUND, hahh", 505

    app.run('0.0.0.0', 5000, debug=True)
