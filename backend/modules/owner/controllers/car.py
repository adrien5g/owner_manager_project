from flask import Blueprint
from flask_pydantic_openapi import FlaskPydanticOpenapi, Response, Request
from flask_pydantic import validate

from ..repository import CarRepository
from ..schemas import (
     GetCarsCount, RegisterOwnerResponse, RegisterCarRequest,
    GetCarColorsResponse, GetCarTypesResponse,
)
from ..ext import (
    CarColorNotFound, CarLimitPerOwnerReached, CarNotFound, CarTypeNotFound,
    EmptyData, InvalidEmail, OwnerNotFound
)

from utils import http_exception, get_doc

class CarController:

    blueprint = Blueprint('cars', __name__, url_prefix='/car')
    doc: FlaskPydanticOpenapi = get_doc()

    @staticmethod
    @blueprint.post('/register')
    @doc.validate(
        body=Request(RegisterCarRequest),
        resp=Response(
            HTTP_200=RegisterOwnerResponse,
            HTTP_400=RegisterOwnerResponse,
            HTTP_403=RegisterOwnerResponse,
            HTTP_404=RegisterOwnerResponse
        ),
        tags=['car']
    )
    @validate()
    def register_car(body: RegisterCarRequest):
        '''
        Register a car in the system
        '''
        car_repository = CarRepository()
        try:
            car_uuid = car_repository.create_car(body)
        except InvalidEmail:
            return http_exception(400, {'status': 'Invalid email'})
        except EmptyData:
            http_exception(404, {'status': 'Please, send a valid data'})
        except CarTypeNotFound:
            http_exception(404, {'status': 'Car type not found'})
        except CarColorNotFound:
            http_exception(404, {'status': 'Car color not found'})
        except OwnerNotFound:
            http_exception(404, {'status': 'Owner not found'})
        except CarLimitPerOwnerReached:
            http_exception(403, {'status': 'Car limit per owner reached'})
        return {
            'status': car_uuid
        }
    
    @staticmethod
    @blueprint.delete('/delete/<car_uuid>')
    @doc.validate(
        resp=Response(
            HTTP_200=RegisterOwnerResponse, 
            HTTP_400=RegisterOwnerResponse,
            HTTP_404=RegisterOwnerResponse
        ),
        tags=['car']
    )
    @validate()
    def delete_car(car_uuid: str):
        '''
        Delete a car from the system
        '''
        car_repository = CarRepository()
        try:
            deleted_car = car_repository.delete_car(car_uuid)
        except CarNotFound:
            http_exception(404, {'status': 'Car not found'})
        return {
            'status': deleted_car
        }

    @staticmethod
    @blueprint.get('/get_types')
    @doc.validate(
        resp=Response(HTTP_200=GetCarTypesResponse),
        tags=['car']
    )
    @validate()
    def get_car_types():
        '''
        Get all available car types registered in the system
        '''
        car_repository = CarRepository()
        car_types = car_repository.get_car_types()
        car_type_names = [car_type.name for car_type in car_types]

        return {
            'car_types': car_type_names
        }
    
    @staticmethod
    @blueprint.get('/get_colors')
    @doc.validate(
        resp=Response(HTTP_200=GetCarColorsResponse),
        tags=['car']
    )
    @validate()
    def get_car_colors():
        '''
        Get all available car colors registered in the system
        '''
        car_repository = CarRepository()
        car_colors = car_repository.get_car_colors()
        car_color_names = [car_color.name for car_color in car_colors]

        return {
            'car_colors': car_color_names
        }

    @staticmethod
    @blueprint.get('/count')
    @doc.validate(
        resp=Response(HTTP_200=GetCarsCount),
        tags=['car']
    )
    @validate()
    def get_car_count():
        '''
        Get the value of cars registered in the system 
        '''
        car_repository = CarRepository()
        cars = car_repository.get_car_count()
        return {
            'car_count': cars
        }