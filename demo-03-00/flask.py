from werkzeug.wrappers import Response


class Flask(object):
    def __init__(self):
        self.debug = False

    def wsgi_app(self, environ, start_response):
        response = Response('hello world', mimetype='text/plain')
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
    app.run('0.0.0.0', 5000, debug=True)
