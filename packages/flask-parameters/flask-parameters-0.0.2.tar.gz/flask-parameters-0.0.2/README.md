# Flask Parameters

This library defines some decorators to be used with [Flask](https://flask.palletsprojects.com/) to inject URL query parameters as arguments into route functions. You can optionally perform type checking of the parameters based on the signature of the route function.

[Documentation](http://flask-params-docs.s3-website-ap-southeast-2.amazonaws.com/)

## Example Usage

```python
import flask

from flask_parameters import inject_query_params
from flask_parameters import inject_and_validate_query_params
from flask_parameters import register_error_handlers

app = flask.Flask(__name__)
register_error_handlers(app)


@app.route("/foo")
@inject_query_params()
def foo(arg, kwarg = 123) -> dict:
    return {"arg": arg, "kwarg": kwarg}


@app.route("/strict_foo")
@inject_and_validate_query_params()
def strict_foo(arg: str, kwarg: int = 123) -> dict:
    return {"arg": arg, "kwarg": kwarg}
```
