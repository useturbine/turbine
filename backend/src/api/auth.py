from functools import wraps
from flask import request, jsonify, make_response, g
from src.db.models import User


def get_user() -> User:
    if "user" not in g:
        raise Exception("User not found in request context")
    return g.user


TurbineAPIKeyHeader = "X-Turbine-Key"


def requires_auth(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get(TurbineAPIKeyHeader)
        if not api_key:
            return make_response(jsonify({"error": "API key missing"}), 401)

        user = User.get_or_none(User.api_key == api_key)
        if not user:
            return make_response(jsonify({"error": "Invalid API key"}), 401)

        g.user = user
        return func(*args, **kwargs)

    return decorated_function
