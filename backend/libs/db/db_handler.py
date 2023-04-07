import os

from sqlmodel import Session, create_engine
from sqlalchemy.future import Engine
from interfaces import Database

class DatabaseHandler(Database):
    def __init__(self) -> None:
        test_string = ''
        if 'API_TEST_ENVIROMENT' in os.environ:
            if os.environ['API_TEST_ENVIROMENT'] == 'true':
                test_string = '_test'

        self.engine = create_engine(f'sqlite:///database{test_string}.sqlite')
        self.session = None

    def get_engine(self) -> Engine:
        return self.engine

    def get_session(self) -> Session:
        self.session = Session(self.engine)
        return self.session

    def __enter__(self) -> Session:
        self.session = Session(self.engine)
        return self.session

    def __exit__(self, *args, **kwargs) -> None:
        self.session.close()
