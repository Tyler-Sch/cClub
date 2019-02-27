from functools import wraps
from user_server.api.models import User
from flask import g, jsonify, request

def login_required(fn):
    @wraps(fn)
    def wrap(*args, **kwargs):
        auth_token = request.headers.get('Authorization')
        if auth_token is None:
            return jsonify({
                'status': 'unauthorized',
                'message': 'must be logged in'
            }), 401
        else:
            u = User.verify_auth_token(auth_token)
            if u is not None:
                g.user = u
            else:
                response = {
                    'status': 'invalid token',
                    'message': 'please login again'
                }
                return jsonify(response), 401

            return fn(*args, **kwargs)
    return wrap
