from flask import Response, request
from models.administrador import Administrador
from functools import wraps
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if not 'auth-token' in request.headers:
            abort(401)
        user = None
        token = request.headers.get('auth-token')
        user = Administrador.load_from_token(token)
        if user is None:
            return Response(error, 401)
        return f(user, *args, **kws)     
    return decorated_function