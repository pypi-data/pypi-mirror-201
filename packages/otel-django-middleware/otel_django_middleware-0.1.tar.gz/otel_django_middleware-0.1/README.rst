OpenTelemetry Django Middleware Tracing
========================================

|pypi|

.. |pypi| image:: https://badge.fury.io/py/otel-django-middleware.svg
   :target: https://pypi.org/project/otel-django-middleware/

This package provides instrumentation that allows for tracing Django middleware functions and class hooks on top of the `opentelemetry-instrumentation-django <https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-django>`_ package.
These include the ``process_request``, ``process_view``, ``process_exception``, ``process_template_response``, ``process_response``, and ``__call__`` methods.

Installation
------------

::

    pip install otel-django-middleware

Instrumenting your Django project
---------------------------------

.. code-block::

    from otel.django.middleware import DjangoMiddlewareInstrumentor

    DjangoMiddlewareInstrumentor().instrument()


Just like the ``opentelemetry-instrumentation-django`` package, when starting your application with ``manage.py`` the ``--noreload`` flag is required to properly inject and instrument the middleware.
