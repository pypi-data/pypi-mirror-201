import flask
import functools
import inspect

from flask_parameters.exceptions import ArgsException
from flask_parameters.type_checking import validate_arguments


def inject_query_params(ignore_args: list[str] = []):
    """
    Decorator that injects URL query parameters into flask a route function.

    Injected parameters will always be strings unless the parameter is not supplied and the default value of a kwarg
    is used. Parameters are always injected as named arguments, so you don't need to be as careful in which order you
    use this decorator.

    :param ignore_args: A list of argument names to ignore when checking for extra and missing arguments in the URL
                        query parameters. E.g. if you have another decorator function injecting arguments.
    :type ignore_args: list[str] = []
    :raise ArgsException: If any missing or extra arguments are supplied in the URL query parameters.
    """

    def constructor(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            sig = inspect.signature(func)
            sig_params = {
                key: param
                for key, param in sig.parameters.items()
                if key not in ignore_args
                # Also ignore URL arguments
                and key not in flask.request.url_rule.arguments
            }

            # Look for extra args
            extra_args = []
            for key in flask.request.args.keys():
                if key not in sig_params:
                    extra_args.append(key)

            # Look for missing args
            missing_args = []
            for key, param in sig_params.items():
                if param.default is inspect._empty and key not in flask.request.args:
                    missing_args.append(key)

            # Uh oh!
            if extra_args or missing_args:
                raise ArgsException(extra_args, missing_args)

            # All good!
            return func(*args, **kwargs, **flask.request.args)

        return wrapper

    return constructor


def inject_and_validate_query_params(ignore_args: list[str] = []):
    """
    An extension of `inject_query_params` that also performs type checking of function arguments based on the signature
    of the function.

    :param ignore_args: A list of argument names to ignore when checking for extra and missing arguments in the URL
                        query parameters. E.g. if you have another decorator function injecting arguments.
    :type ignore_args: list[str] = []
    :raise ArgsException: If any missing or extra arguments are supplied in the URL query parameters.
    :raise TypeCheckException: If any arguments fail the type check.
    """

    def constructor(func):
        return inject_query_params(ignore_args=ignore_args)(validate_arguments(func))

    return constructor
