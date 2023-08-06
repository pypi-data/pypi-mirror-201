from django.conf import settings
from django.core.handlers.base import BaseHandler
from functools import wraps
import importlib
from opentelemetry import trace
from opentelemetry.trace import SpanKind
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from otel.django.middleware.package import _instruments
from opentelemetry.instrumentation.django import _get_django_middleware_setting
from types import FunctionType


_CLASS_HOOKS = [
    "process_exception",
    "process_request",
    "process_response",
    "process_view",
    "process_template_response",
    "__call__",
]


def span_wrap_function(func, name, attributes=None):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with trace.get_tracer(__name__).start_as_current_span(
                name=name, kind=SpanKind.CLIENT, attributes=attributes
            ) as span:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    span.set_attribute("error", True)
                    span.record_exception(e)
                    raise

        return wrapper


def trace_middleware():
    settings_middleware = getattr(settings, _get_django_middleware_setting())
    excluded_middleware = getattr(settings, "TRACE_EXCLUDED_MIDDLEWARE", set())
    excluded_middleware.add('opentelemetry.instrumentation.django.middleware.otel_middleware._DjangoMiddleware')

    for path in settings_middleware:
        if path in excluded_middleware:
            continue

        module_path, attribute = path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        middleware = getattr(module, attribute)

        if hasattr(middleware, "traced_middleware"):
            continue

        if (isinstance(middleware, FunctionType)):
            wrapper = span_wrap_function(middleware, path)
            wrapper.traced_middleware = True
            setattr(module, attribute, wrapper)

        elif (isinstance(middleware, type)):
            for hook in _CLASS_HOOKS:
                if hasattr(middleware, hook):
                    wrapper = span_wrap_function(getattr(middleware, hook), f"{path}.{hook}")
                    wrapper.traced_middleware = True
                    setattr(middleware, hook, wrapper)


class DjangoMiddlewareInstrumentor(BaseInstrumentor):
    def instrumentation_dependencies(self):
        return _instruments
    

    def _instrument(self):
        @wraps(BaseHandler.load_middleware)
        def load_middleware(self, *args, **kwargs):
            trace_middleware()
            return BaseHandler.load_middleware.__wrapped__(self, *args, **kwargs)


        load_middleware.traced_middleware = True
        BaseHandler.load_middleware = load_middleware


    def _uninstrument(self):
        if getattr(BaseHandler.load_middleware, "traced_middleware", False):
            BaseHandler.load_middleware = BaseHandler.load_middleware.__wrapped__

        settings_middleware = getattr(settings, _get_django_middleware_setting())

        for path in settings_middleware:
            module_path, attribute = path.rsplit(".", 1)
            module = importlib.import_module(module_path)
            middleware = getattr(module, attribute)

            if not getattr(middleware, "traced_middleware", False):
                continue

            if (isinstance(middleware, FunctionType)):
                setattr(module, attribute, middleware.__wrapped__)

            elif (isinstance(middleware, type)):
                for hook in _CLASS_HOOKS:
                    if hasattr(middleware, hook):
                        setattr(middleware, hook, getattr(middleware, hook).__wrapped__)
