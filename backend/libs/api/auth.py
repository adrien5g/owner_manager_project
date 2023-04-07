from datetime import datetime, timedelta

import jwt
from jwt.exceptions import ExpiredSignatureError
from pydantic import ValidationError

from utils import http_exception

secret_key = 'data'
jwt_algorithm = 'HS256'
access_token_expire_in_minutes = 120

def create_access_token(subject: str, expires_delta:int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=access_token_expire_in_minutes)

    to_encode = {'exp': expires_delta, 'sub':str(subject)}
    enconded_jwt = jwt.encode(to_encode, secret_key, jwt_algorithm)
    return enconded_jwt

def verify_if_is_auth(token: str):
    def decode_jwt(token: str):
        token = token.replace('Bearer', '').strip()
        return jwt.decode(
            token, secret_key, algorithms=[jwt_algorithm]
        )
    try:
        payload = decode_jwt(token)
    except(jwt.PyJWKError, ValidationError, jwt.DecodeError):
        http_exception(403, {'status': 'Could not validate credentials'})
    except ExpiredSignatureError:
        http_exception(403, {'status': 'JWT signature has expired'})
    return payload['sub']
