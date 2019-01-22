from werkzeug.wrappers import Request, Response
from werkzeug.local import LocalStack, LocalProxy


class FlaskRequest(Request):
    pass


class _RequestContext(object):
    def __init__(self, app, environ):
        self.app = app
        self.request = app.request_class(environ)


class Flask(object):
    request_class = FlaskRequest

    def __init__(self, name):
        self.debug = False
        self.name = name

    def wsgi_app(self, environ, start_response):
        _request_ctx_stack.push(_RequestContext(self, environ))
        try:
            response = Response('[%s] hello %s' % (
                current_app.name, request.args.get('name', 'world')),
                mimetype='text/plain')
            return response(environ, start_response)
        finally:
            _request_ctx_stack.pop()

    def run(self, host='localhost', port=5000, **options):
        from werkzeug.serving import run_simple
        if 'debug' in options:
            self.debug = options.pop('debug')
        options.setdefault('use_reloader', self.debug)
        options.setdefault('use_debugger', self.debug)
        run_simple(host, port, self, **options)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


_request_ctx_stack = LocalStack()
current_app = LocalProxy(lambda: _request_ctx_stack.top.app)
request = LocalProxy(lambda: _request_ctx_stack.top.request)

if __name__ == '__main__':
    app = Flask(__name__)
    app.run(host='0.0.0.0', port=8000, debug=True)
