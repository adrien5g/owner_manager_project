from flask import Blueprint
from flask_pydantic_openapi import FlaskPydanticOpenapi, Response, Request
from flask_pydantic import validate

from .repository import UserRepository
from .schemas import ErrorAuth, UserAuth, AccessToken
from .ext import UserNotFound, WrongPassword

from utils import http_exception, get_doc
from libs.api.auth import create_access_token

class UserController:
    blueprint = Blueprint('users', __name__, url_prefix='/user')
    doc: FlaskPydanticOpenapi = get_doc()

    @staticmethod
    @blueprint.post('/login')
    @doc.validate(
        body=Request(UserAuth),
        resp=Response(
            HTTP_200=AccessToken, HTTP_404=ErrorAuth
        ),
        tags=['user']
    )
    @validate()
    def user_login(body: UserAuth):
        '''
        Login user
        '''
        user_repository = UserRepository()
        try:
            user = user_repository.login_user(body)
        except UserNotFound:
            http_exception(404, {'status': 'User not found'})
        except WrongPassword:
            http_exception(404, {'status': 'Wrong password'})
        access_token = create_access_token(user.id)

        return AccessToken(access_token=access_token)