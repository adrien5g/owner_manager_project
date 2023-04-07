import os
from libs.api import ApiHandler
from modules.owner.controllers import OwnerController, CarController
from modules.user.controller import UserController
from middlewares import auth_middleware
from utils import boostrap

class Service:

    def __init__(self, test_enviroment: bool = False) -> None:
        if test_enviroment:
            os.environ['API_TEST_ENVIROMENT'] = 'true'
        boostrap()
        self.api = ApiHandler()
        self.api.register_blueprint(UserController.blueprint)
        self.api.register_blueprint(OwnerController.blueprint)
        self.api.register_blueprint(CarController.blueprint)
        self.api.register_middleware(auth_middleware)
    
    def start(self):
        self.api.start()

if __name__ == '__main__':
    service = Service()
    service.start()
