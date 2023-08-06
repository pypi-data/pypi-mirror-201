import json

from flask import Flask
from flask import jsonify
from typing import Any


class TypeCheckException(Exception):
    """
    Some arguments failed the type check.

    :param errors: Contains information about the type errors.
    :type errors: dict
    """

    def __init__(self, errors: dict):
        self.errors = errors


class ArgsException(Exception):
    """
    Missing or extra arguments are supplied in the URL query parameters.

    :param extra_args: Names of supplied arguments not in the function signature.
    :type extra_args: list[str]
    :param missing_args: Names of the missing required arguments.
    :type missing_args: list[str]
    """

    def __init__(self, extra_args: list[str], missing_args: list[str]):
        self.extra_args = extra_args
        self.missing_args = missing_args


class _TypeJsonEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if type(o) == type:
            return str(o)
        return super().default(o)


def register_error_handlers(app: Flask):
    """
    Register error handlers on the flask app for the flask_parameters exceptions.

    TypeCheckException and ArgsException will both return an HTTP status code of 400 with a JSON response.

    :param app: Flask app to register error handlers on.
    """

    @app.errorhandler(TypeCheckException)
    def handle_validation_error(e: TypeCheckException):
        # don't want to go adding a custom json encoder to the entire flask application
        return (
            jsonify(
                json.loads(json.dumps({"type_errors": e.errors}, cls=_TypeJsonEncoder))
            ),
            400,
        )

    @app.errorhandler(ArgsException)
    def handle_validation_error(e: ArgsException):
        res = {}
        if e.extra_args:
            res["extra_args"] = e.extra_args
        if e.missing_args:
            res["missing_args"] = e.missing_args
        return jsonify(res), 400
