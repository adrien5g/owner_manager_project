from sqlmodel import select

from .schemas import UserAuth
from .models import UserModel
from .ext import UserNotFound, WrongPassword

from libs.db import DatabaseHandler
from utils import verify_password

class UserRepository:

    @staticmethod
    def login_user(data: UserAuth) -> UserModel:
        with DatabaseHandler() as session:
            query = select(UserModel).where(UserModel.username == data.username)
            user = session.exec(query).first()
            if not user:
                raise UserNotFound
            
            if not verify_password(user.password, data.password):
                raise WrongPassword
            
            return user
