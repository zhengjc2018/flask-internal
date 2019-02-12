from werkzeug.wrappers import Response


def err_handle(func):
    def wrapper(*args, **options):
        try:
            return func(*args, **options)
        except Exception as e:
            # start_response('200 OK', [('Content-Type', 'text/html')])
            # abort(404)
            response = Response(e.message.encode('utf-8'))
            response.status_code = e.code
            response.content_type = 'text/html'
            return [response]
    return wrapper


class MyExceptions(Exception):
    code = 405
    message = 'just for fun1'
