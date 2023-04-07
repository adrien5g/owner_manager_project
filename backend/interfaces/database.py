from abc import ABC, abstractclassmethod

from sqlmodel import Session

class Database(ABC):

    @abstractclassmethod
    def get_session(self):
        pass

    @abstractclassmethod
    def __init__(self) -> Session:
        pass

    @abstractclassmethod
    def __exit__(self, *args, **kwargs) -> None:
        pass
