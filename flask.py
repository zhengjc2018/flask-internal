from werkzeug.wrappers import Request, Response
from werkzeug.local import LocalStack, LocalProxy
from werkzeug.routing import Map, Rule
from werkzeug.contrib.securecookie import SecureCookie


class FlaskRequest(Request):
    pass


class FlaskResponse(Response):
    default_mimetype = 'text/html'


class _RequestContext(object):
    def __init__(self, app, environ):
        self.app = app
        self.request = app.request_class(environ)
        self.session = app.open_session(self.request)
        self.url_adapter = app.url_map.bind_to_environ(environ)


class Flask(object):
    request_class = FlaskRequest
    response_class = FlaskResponse

    secret_key = None
    session_cookie_name = 'flask_session'

    def __init__(self, name):
        self.debug = False
        self.name = name
        self.url_map = Map()
        self.view_functions = {}
        self.blueprints = {}

    def dispatch_request(self):
        endpoint, values = _request_ctx_stack.top.url_adapter.match()
        return self.view_functions[endpoint](**values)

    def make_response(self, response):
        session = _request_ctx_stack.top.session
        self.save_session(session, response)
        return response

    def open_session(self, request):
        if self.secret_key is not None:
            return SecureCookie.load_cookie(request,
                                            key=self.session_cookie_name,
                                            secret_key=self.secret_key)

    def save_session(self, session, response):
        if session is not None:
            session.save_cookie(response, key=self.session_cookie_name)

    def add_url_rule(self, rule, endpoint, view_func, **options):
        options['endpoint'] = endpoint
        self.url_map.add(Rule(rule, **options))
        self.view_functions[options['endpoint']] = view_func

    def register_blueprint(self, blueprint, **options):
        self.blueprints[blueprint.name] = blueprint
        blueprint.register(self, **options)

    def route(self, rule, **options):
        def decorator(f):
            endpoint = options.get("endpoint", f.__name__)
            self.add_url_rule(rule, endpoint, f, **options)
            return f
        return decorator

    def wsgi_app(self, environ, start_response):
        _request_ctx_stack.push(_RequestContext(self, environ))
        try:
            rv = self.dispatch_request()
            response = self.response_class(rv)
            response = self.make_response(response)
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


class BlueprintSetupState(object):
    def __init__(self, blueprint, app, **options):
        self.blueprint = blueprint
        self.app = app
        self.url_prefix = options.get('url_prefix',
                                      '/%s' % self.blueprint.name)

    def add_url_rule(self, rule, endpoint, view_func, **options):
        rule = '/'.join((self.url_prefix, rule.lstrip('/')))
        endpoint = '%s.%s' % (self.blueprint.name, endpoint)
        self.app.add_url_rule(rule, endpoint, view_func, **options)


class Blueprint(object):
    def __init__(self, name):
        self.name = name
        self.deferred_functions = []

    def register(self, app, **options):
        state = BlueprintSetupState(self, app, **options)
        for deferred in self.deferred_functions:
            deferred(state)

    def record(self, func):
        self.deferred_functions.append(func)

    def add_url_rule(self, rule, endpoint, view_func, **options):
        self.record(lambda s: s.add_url_rule(rule, endpoint, view_func,
                                             **options))

    def route(self, rule, **options):
        def decorator(f):
            endpoint = options.get("endpoint", f.__name__)
            self.add_url_rule(rule, endpoint, f, **options)
            return f
        return decorator


if __name__ == '__main__':
    bp = Blueprint('foo')

    @bp.route('/hello/<name>', methods=['GET'])
    def foo_hello(name):
        return 'foo hello %s' % name

    app = Flask(__name__)
    app.secret_key = 'this_is_secret_key'

    @app.route('/hello/<name>', methods=['GET'])
    def hello(name):
        return 'hello %s' % name

    app.register_blueprint(bp)

    app.run(host='0.0.0.0', port=8000, debug=True)
