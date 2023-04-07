from typing import List
from sqlmodel import select, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import not_

from .schemas import RegisterOwnerRequest, RegisterCarRequest
from .models import OwnerModel, CarTypeModel, CarColorModel, CarModel
from .ext import (
    CarLimitPerOwnerReached, CarNotFound, EmailAlreadyInUse, InvalidEmail, InvalidName,
    EmptyData, CarColorNotFound, CarTypeNotFound, OwnerNotFound
)

from libs.db import DatabaseHandler
from utils import email_is_valid

class OwnerRepository:

    @staticmethod
    def register_owner(data: RegisterOwnerRequest) -> OwnerModel:
        with DatabaseHandler() as session:
            if not email_is_valid(data.email):
                raise InvalidEmail
            
            if data.name.strip() == '':
                raise InvalidName
            
            query = select(OwnerModel).where(OwnerModel.email == data.email)
            user = session.exec(query).first()
            if user:
                raise EmailAlreadyInUse
            
            new_owner = OwnerModel.from_orm(data)
            session.add(new_owner)
            session.commit()
        return new_owner
    
    @staticmethod
    def get_about_owner(owner_email: str) -> OwnerModel:
        with DatabaseHandler() as session:
            query = select(OwnerModel).where(OwnerModel.email == owner_email)
            owner = session.exec(query).first()
            if not owner:
                raise OwnerNotFound
            return owner
        
    @staticmethod
    def get_all_owners(sale_opportunity: bool = False) -> List[OwnerModel]:
        with DatabaseHandler() as session:
            query = select(OwnerModel).options(joinedload(OwnerModel.cars))
            if sale_opportunity:
                subquery = select(CarModel.owner).distinct()
                query = query.where(not_(OwnerModel.id.in_(subquery)))
            owners = session.exec(query).unique().all()
            return owners
        
    @staticmethod
    def delete_owner(owner_email: str) -> bool:
        with DatabaseHandler() as session:
            query = select(OwnerModel).where(OwnerModel.email == owner_email)
            owner = session.exec(query).first()

            if not owner:
                raise OwnerNotFound

            query = delete(CarModel).where(CarModel.owner == owner.id)
            session.exec(query)
            session.commit()
            session.delete(owner)
            session.commit()
            return True

    @staticmethod
    def get_owner_count() -> int:
        with DatabaseHandler() as session:
            query = select(OwnerModel)
            cars = session.exec(query).all()
            return len(cars)

class CarRepository:

    @staticmethod
    def create_car(data: RegisterCarRequest) -> str:
        with DatabaseHandler() as session:
            if not email_is_valid(data.owner_email):
                raise InvalidEmail
            
            if all([data.car_color.strip() == '', data.car_type.strip() == '']):
                raise EmptyData

            query = select(CarTypeModel).where(CarTypeModel.name == data.car_type)
            car_type = session.exec(query).first()
            if not car_type:
                raise CarTypeNotFound
            
            query = select(CarColorModel).where(CarColorModel.name == data.car_color)
            car_color = session.exec(query).first()
            if not car_color:
                raise CarColorNotFound
            
            query = select(OwnerModel).where(OwnerModel.email == data.owner_email)
            owner = session.exec(query).first()
            if not owner:
                raise OwnerNotFound
            
            query = select(CarModel).where(CarModel.owner == owner.id)
            cars_by_owner = session.exec(query).all()
            if not len(cars_by_owner) < 3:
                raise CarLimitPerOwnerReached
            
            new_car = CarModel(
                color=car_color.id, type=car_type.id, owner=owner.id
            )
            session.add(new_car)
            session.commit()
            return new_car.uuid
    
    @staticmethod
    def get_car_types() -> List[CarTypeModel]:
        with DatabaseHandler() as session:
            query = select(CarTypeModel)
            car_types = session.exec(query).all()
            return car_types
        
    @staticmethod
    def get_car_colors() -> List[CarColorModel]:
        with DatabaseHandler() as session:
            query = select(CarColorModel)
            car_colors = session.exec(query).all()
            return car_colors
        
    @staticmethod
    def delete_car(car_uuid: str) -> str:
        with DatabaseHandler() as session:
            query = select(CarModel).where(CarModel.uuid == car_uuid)
            selected_car = session.exec(query).first()
            if not selected_car:
                raise CarNotFound
            
            session.delete(selected_car)
            session.commit()
            return car_uuid
        
    @staticmethod
    def get_cars_by_owner(owner: OwnerModel) -> List[CarModel]:
        with DatabaseHandler() as session:
            query = select(CarModel).where(CarModel.owner == owner.id)\
                .options(joinedload(CarModel.car_color), joinedload(CarModel.car_type))
            cars = session.exec(query).all()
            return cars
        
    @staticmethod
    def get_car_count() -> int:
        with DatabaseHandler() as session:
            query = select(CarModel)
            cars = session.exec(query).all()
            return len(cars)