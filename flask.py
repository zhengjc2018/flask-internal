from werkzeug.wrappers import Response


class Flask(object):
    def __init__(self, **options):
        pass

    def wsgi_app(self, environ, start_response):
        response = Response('hello world', mimetype='text/plain')
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


if __name__ == '__main__':
    from werkzeug.serving import run_simple

    app = Flask()
    run_simple('0.0.0.0', 8000, app, use_reloader=True, use_debugger=True)
