"""
    Muffin-Classy
    ------------

    Class based views for the Muffin web framework.

    Inspired by Flask-Classy.

"""
import functools
import inspect
import logging

from aiohttp.hdrs import METH_ANY


__version__ = "0.0.0"


logger = logging.getLogger(__name__)


def route(path=None, methods=None, name=None):
    def decorator(func):
        if not hasattr(func, '_classy'):
            func._classy = []
        func._classy.append({
            'path': path,
            'methods': methods,
            'name': name,
        })
        return func
    return decorator


class BaseView(object):
    """Base view for any class based views implemented with Muffin-Classy. Will
    automatically configure routes when registered with a Muffin app instance.
    """

    _root_methods = {
        "get": ["GET"],
        "put": ["PUT"],
        "patch": ["PATCH"],
        "post": ["POST"],
        "delete": ["DELETE"],
        "index": ["GET"],
    }

    @classmethod
    def register(cls, app, base_path):
        """Register View class in Muffin application.

        This generates routes for defined class methods, and adds them to
        application router.
        """

        members = get_interesting_members(MuffinView, cls)

        delayed = []

        def delay(path, route_name, http_methods, handler):

            def closure():
                cls._register(app, handler, path, route_name, http_methods)

            delayed.append(closure)

        def _register(opts):

            route_name = opts.get('name')
            if route_name is None:
                route_name = cls._build_route_name(method_name)

            if method_name in cls._root_methods:
                http_methods = cls._root_methods[method_name]
                path = cls._method_path(base_path, value)
                delay(path, route_name, http_methods, handler)
            else:
                http_methods = opts.get('methods')
                if opts.get('path') is not None:
                    path = opts['path']
                else:
                    path = method_name
                path = '%s/%s' % (base_path.rstrip('/'), path.strip('/'))
                path = cls._method_path(path, value)
                if http_methods is None:
                    cls._register(app, handler, path, route_name)
                else:
                    cls._register(app, handler, path, route_name, http_methods)

        for method_name, value in members:
            handler = cls._proxy_method_factory(method_name)
            opts_list = getattr(value, '_classy', [{}])
            for opts in opts_list:
                _register(opts)

        for i in delayed:
            i()

    @classmethod
    def _proxy_method_factory(cls, name):
        """Creates a proxy function that can be used by Muffin routing. The
        proxy instantiates the MuffinView subclass and calls the appropriate
        method.

        :param name: the name of the method to create a proxy for
        """

        self = cls()
        view = getattr(self, name)

        @functools.wraps(view)
        def proxy(request, *args, **kwargs):

            request.classy_method_name = name

            if hasattr(self, "before_request"):
                response = self.before_request(request)
                if response is not None:
                    return response

            before_view_name = "before_" + name
            if hasattr(self, before_view_name):
                before_view = getattr(self, before_view_name)
                response = before_view(request)
                if response is not None:
                    return response

            response = view(request, **request.match_info)

            after_view_name = "after_" + name
            if hasattr(self, after_view_name):
                after_view = getattr(self, after_view_name)
                response = after_view(request, response)

            if hasattr(self, "after_request"):
                response = self.after_request(request, response)

            return response

        return proxy

    @classmethod
    def _method_path(cls, base_path, method):

        parts = [base_path.rstrip('/') or '/']

        try:
            argspec = get_true_argspec(method)
        except DecoratorCompatibilityError:
            raise DecoratorCompatibilityError(
                "Can't get method arguments on %s in class %s: bad decorator" % (
                    base_path, cls.__name__
                ))

        parts.extend(["{%s}" % arg for arg in argspec[0][2:]])

        return "/".join(parts)

    @classmethod
    def _build_route_name(cls, method_name):
        """Creates a unique route name based on the combination of the class
        name with the method name.

        :param method_name: the method name to use when building a route name
        """
        return cls.__name__ + ":%s" % method_name


class MuffinView(BaseView):
    @classmethod
    def _register(cls, app, handler, path, route_name, http_methods=None):
        if http_methods is None:
            app.register(path, name=route_name)(handler)
        else:
            app.register(path, name=route_name, methods=http_methods)(handler)


class AIOHttpView(BaseView):
    @classmethod
    def _register(cls, app, handler, path, route_name, http_methods=None):
        if http_methods is None:
            http_methods = [METH_ANY]
        for method in http_methods:
            app.router.add_route(method, path, handler, name=route_name)


def get_interesting_members(base_class, cls):
    """Returns a list of methods that can be routed to"""

    base_members = dir(base_class)
    all_members = inspect.getmembers(cls, predicate=inspect.isfunction)

    def is_interesting(member):

        if member[0] in base_members:
            return False

        if member[0].startswith(("_", "before_", "after_")):
            return False

        return True

    return [i for i in all_members if is_interesting(i)]


def get_true_argspec(method):
    """Drills through layers of decorators attempting to locate the actual
    argspec for the method."""

    argspec = inspect.getargspec(method)
    args = argspec[0]
    if args and args[0] == 'self':
        return argspec
    if hasattr(method, '__func__'):
        method = method.__func__
    if not hasattr(method, '__closure__') or method.__closure__ is None:
        raise DecoratorCompatibilityError

    closure = method.__closure__
    for cell in closure:
        inner_method = cell.cell_contents
        if inner_method is method:
            continue
        if not inspect.isfunction(inner_method) \
                and not inspect.ismethod(inner_method):
            continue
        true_argspec = get_true_argspec(inner_method)
        if true_argspec:
            return true_argspec


class DecoratorCompatibilityError(Exception):
    pass
