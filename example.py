from muffin import Application
from muffin_classy import MuffinView, route
from functools import wraps

VALUE1 = "value1"


def get_value():
    return VALUE1


app = Application('example')


class IndexView(MuffinView):

    def index(self, request):
        """A docstring for testing that docstrings are set"""
        return "Index"

IndexView.register(app, "/")


class BasicView(MuffinView):

    def index(self, request):
        return "Index"

    def get(self, request, obj_id):
        return "Get " + obj_id

    async def put(self, request, id):
        return "Put %s: %s" % (id, (await request.content.read()).decode('ascii'))

    async def post(self, request):
        return "Post: %s" % (await request.content.read()).decode('ascii')

    def custom_method(self, request):
        return "Custom Method"

    def custom_method_with_params(self, request, p_one, p_two):
        return "Custom Method %s %s" % (p_one, p_two)

    @route("/routed/")
    def routed_method(self, request):
        return "Routed Method"

    @route("/route1/")
    @route("/route2/")
    def multi_routed_method(self, request):
        return "Multi Routed Method"

    @route("/noslash")
    def no_slash_method(self, request):
        return "No Slash Method"

    @route("/endpoint/", name="foobar")
    def custom_endpoint(self, request, param):
        return "Custom Endpoint"

    @route("/route3/", methods=['POST'])
    def custom_http_method(self, request):
        return "Custom HTTP Method"


BasicView.register(app, '/basic')


class PostView(MuffinView):

    def post(self, request):
        return "Custom HTTP Method"

    @route(methods=['POST'])
    def check(self, request):
        return "Check"


PostView.register(app, '/post')


class BeforeRequestView(MuffinView):

    def before_request(self, request):
        self.response = "Before Request"

    def index(self, request):
        return self.response


BeforeRequestView.register(app, '/before_request')


class BeforeViewView(MuffinView):

    def before_index(self, request):
        self.response = "Before View"

    def index(self, request):
        return self.response


BeforeViewView.register(app, '/before_view')


class BeforeRequestReturnsView(MuffinView):

    def before_request(self, request):
        return "BEFORE"

    def index(self, request):
        return "Should never see this"


BeforeRequestReturnsView.register(app, '/before_request_returns')


class BeforeViewReturnsView(MuffinView):

    def before_index(self, request):
        return "BEFORE"

    def index(self, request):
        return "Should never see this"


BeforeViewReturnsView.register(app, '/before_view_returns')


class AfterViewView(MuffinView):

    def after_index(self, request, response):
        return "After View"

    def index(self, request):
        return "Index"


AfterViewView.register(app, '/after_view')


class AfterRequestView(MuffinView):

    def after_request(self, request, response):
        return "After Request"

    def index(self, request):
        return "Index"


AfterRequestView.register(app, '/after_request')


class VariedMethodsView(MuffinView):

    def index(self, request):
        return "Index"

    @route("/routed/")
    def routed_method(self, request):
        return "Routed Method"

    @classmethod
    def class_method(cls):
        return "Class Method"


VariedMethodsView.register(app, '/varied')


class SubVariedMethodsView(VariedMethodsView):
    pass


SubVariedMethodsView.register(app, '/subvaried')


def func_decorator(f):
    def decorated_view(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_view


def wraps_decorator(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_view


def params_decorator(p_1, p_2):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def recursive_decorator(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        decorated_view.foo()
        return f(*args, **kwargs)

    def foo():
        return 'bar'
    decorated_view.foo = foo

    return decorated_view


def more_recursive(stop_type):
    def _inner(func):
        def _recursive(*args, **kw):
            return func(*args, **kw)
        return _recursive
    return _inner


class DecoratedView(MuffinView):

    @func_decorator
    def index(self, request):
        return "Index"

    @func_decorator
    def get(self, request, id):
        return "Get " + id

    @recursive_decorator
    def post(self, request):
        return "Post"

    @params_decorator("oneval", "anotherval")
    def params_decorator_method(self, request):
        return "Params Decorator"

    @params_decorator(get_value(), "value")
    def delete(self, request, obj_id):
        return "Params Decorator Delete " + obj_id

    @more_recursive(None)
    def get_some(self, request):
        return "Get Some"

    @more_recursive(None)
    @recursive_decorator
    def get_this(self, request):
        return "Get This"

    @route('/mixitup')
    @more_recursive(None)
    @recursive_decorator
    def mixitup(self, request):
        return "Mix It Up"

    @more_recursive(None)
    def someval(self, request, val):
        return "Someval " + val

    @route('/anotherval/<val>')
    @more_recursive(None)
    @recursive_decorator
    def anotherval(self, request, val):
        return "Anotherval " + val


DecoratedView.register(app, '/decorated')


class InheritanceView(BasicView):

    # Tests method override
    def get(self, request, obj_id):
        return "Inheritance Get " + obj_id

    @route('/<obj_id>/delete', methods=['DELETE'])
    def delete(self, request, obj_id):
        return "Inheritance Delete " + obj_id

    @route('/with_route')
    def with_route(self, request):
        return "Inheritance with route"


InheritanceView.register(app, '/inherit')


class DecoratedInheritanceView(DecoratedView):

    @recursive_decorator
    def get(self, request, obj_id):
        return "Decorated Inheritance Get " + obj_id


DecoratedInheritanceView.register(app, '/decor_inherit')
