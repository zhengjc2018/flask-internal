from werkzeug.wrappers import Request, Response


class Flask(object):
    def __init__(self):
        self.debug = False

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = Response('hello %s' % request.args.get('name', 'world'),
                            mimetype='text/plain')
        return response(environ, start_response)

    def run(self, host='localhost', port=5000, **options):
        from werkzeug.serving import run_simple
        if 'debug' in options:
            self.debug = options.pop('debug')
        options.setdefault('use_reloader', self.debug)
        options.setdefault('use_debugger', self.debug)
        run_simple(host, port, self, **options)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


if __name__ == '__main__':
    app = Flask()
    app.run(host='0.0.0.0', port=8000, debug=True)
