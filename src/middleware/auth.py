from functools import wraps
from flask import request, abort

from constants.response_status_codes import ResponseStatusCodes
from constants.env import Env

class HeaderKeys:
    AUTHORIZATION = 'Authorization'

def require_api_key(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get(HeaderKeys.AUTHORIZATION, '').removeprefix('Bearer ')
        if token != Env.API_SECRET:
            abort(ResponseStatusCodes.UNAUTHORIZED)
        return func(*args, **kwargs)
    return decorated
