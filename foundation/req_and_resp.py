from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple


# http://werkzeug.pocoo.org/docs/quickstart/
def wsgi_app(environ, start_response):
    print('environ: %s' % environ)
    request = Request(environ)
    print('request: %s' % request.__dict__)
    response = Response('hello world', mimetype='text/plain')
    print('response: %s' % response.__dict__)
    return response(environ, start_response)


run_simple('0.0.0.0', 8000, wsgi_app)
