from datetime import datetime, timedelta
import calendar
from functools import wraps

from flask import jsonify,g,request
import jwt
from jwt import DecodeError, ExpiredSignature,InvalidIssuedAtError

from config import Config
from custom_exceptions import AuthError


def create_token(scopes):

    print(scopes)

    payload={'scopes':scopes,
             'aud':'usr',
             'iat': calendar.timegm(datetime.utcnow().timetuple()),
             'exp': calendar.timegm((datetime.utcnow() + timedelta(hours=12)).timetuple()),
             'iss': 'imdb_task'
             }


    token=jwt.encode(payload=payload,key=Config.JWT.SECRET_KEY,algorithm=Config.JWT.ALGORITHM)

    return token.decode('unicode_escape')


def parse_token(req):
    token = req.headers.get('Authorization')
    return jwt.decode(token, Config.JWT.SECRET_KEY, algorithms=Config.JWT.ALGORITHM,audience='usr')

def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.headers.get('Authorization'):
                raise AuthError('Missing Authorization Header',401)
            try:
                g.token_data=parse_token(request)
            except (DecodeError,InvalidIssuedAtError):
                raise AuthError('Token is invalid',401)
            except ExpiredSignature:
                raise AuthError('Token has expired',401)
            return f(*args, **kwargs)
        return decorated_function

def check_scope(*args1, **kwargs1):
    def scope_decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print(kwargs1)
            found_scope=0
            for scope_token in g.token_data['scopes']:
                if kwargs1['scope_required']==scope_token:
                    found_scope=1
                    break
            if found_scope==0:
                raise AuthError('Insufficient permissions',401)
            return f(*args, **kwargs)
        return decorated_function
    return scope_decorator






