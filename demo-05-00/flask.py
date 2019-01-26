from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule

# 参考：
# http://werkzeug.pocoo.org/docs/routing/#quickstart


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
        rv = self.dispatch_request(environ)
        response = self.response_class(rv)
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
        return 'hello %s' % user

    app.run('0.0.0.0', 5000, debug=True)
