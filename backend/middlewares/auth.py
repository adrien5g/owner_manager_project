from flask import request
from utils import http_exception
from libs.api.auth import verify_if_is_auth

def auth_middleware():
    allowed_endpoints = ['/user/login', '/apidoc/redoc', 'apidoc/openapi.json']
    if any([end in request.path for end in allowed_endpoints]):
        return
    if not 'Authorization' in request.headers:
        http_exception(403, {'status': 'No token found'})
    verify_if_is_auth(request.headers['Authorization'])