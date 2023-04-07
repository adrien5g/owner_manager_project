from os import path, environ

from sqlmodel import SQLModel

from libs.db import DatabaseHandler
from modules.user.models import UserModel
from modules.owner.models import CarTypeModel, CarColorModel
from .crypt import crypt_password

def boostrap():
    test_enviroment = False
    if 'API_TEST_ENVIROMENT' in environ:
        if environ['API_TEST_ENVIROMENT'] == 'true':
            test_enviroment = True
    
    if path.isfile('database.sqlite') and not test_enviroment:
        return

    database = DatabaseHandler()
    SQLModel.metadata.create_all(database.get_engine())

    car_colors = [
        CarColorModel(name='yellow'),
        CarColorModel(name='blue'),
        CarColorModel(name='gray')
    ]

    car_types = [
        CarTypeModel(name='hatch'),
        CarTypeModel(name='sedan'),
        CarTypeModel(name='convertible')
    ]
    admin_user = UserModel(username='admin', password=crypt_password('admin'))
    with DatabaseHandler() as session:
        session.add_all([*car_types, *car_colors, admin_user])
        session.commit()
        
