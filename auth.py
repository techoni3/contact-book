import functools
from utils import resp_fail
from flask import request

def check_user_and_password(username, password):
    from app import app
    return username == app.config['USERNAME'] and password == app.config['PASSWORD']


def authorize(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_user_and_password(auth.username, auth.password):
            return resp_fail("Unauthorized access", status_code=401)
        return f(*args, **kwargs)
    return decorated