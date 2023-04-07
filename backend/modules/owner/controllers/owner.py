from flask import Blueprint, request
from flask_pydantic_openapi import FlaskPydanticOpenapi, Response, Request
from flask_pydantic import validate

from ..repository import OwnerRepository, CarRepository
from ..schemas import (
    AboutOwnerWithCars, DeleteOwnerResponse, GetOwnersCount, ListAboutUser, OwnerFilter, RegisterOwnerRequest, RegisterOwnerResponse,
    GetListOfOwners
)
from ..ext import (
    EmailAlreadyInUse, InvalidEmail, InvalidName, OwnerNotFound
)

from utils import http_exception, get_doc

class OwnerController:

    blueprint = Blueprint('owners', __name__, url_prefix='/owner')
    doc: FlaskPydanticOpenapi = get_doc()

    @staticmethod
    @blueprint.post('/register')
    @doc.validate(
        body=Request(RegisterOwnerRequest),
        resp=Response(
            HTTP_200=RegisterOwnerResponse, 
            HTTP_400=RegisterOwnerResponse,
            HTTP_409=RegisterOwnerResponse
        ),
        tags=['owner']
    )
    @validate()
    def register_owner(body: RegisterOwnerRequest):
        '''
        Register an owner in the system
        '''
        owner_repository = OwnerRepository()
        try:
            owner_repository.register_owner(body)
        except InvalidEmail:
            return http_exception(400, {'status': 'Invalid email'})
        except InvalidName:
            return http_exception(400, {'status': 'Invalid name'})
        except EmailAlreadyInUse:
            return http_exception(409, {'status': 'Email in use'})
        return {
            'status': True
        }
    
    @staticmethod
    @blueprint.get('/about/<owner_email>')
    @doc.validate(
        resp=Response(
        HTTP_200=AboutOwnerWithCars,
        HTTP_400=RegisterOwnerResponse,
        HTTP_404=RegisterOwnerResponse
        ),
        tags=['owner']
    )
    @validate()
    def get_about_owner(owner_email: str):
        '''
        Get data from a specific owner
        '''
        owner_repository = OwnerRepository()
        car_repository = CarRepository()
        try:
            owner = owner_repository.get_about_owner(owner_email)
        except OwnerNotFound:
            http_exception(404, {'status': 'Owner not found'})
        list_of_cars = car_repository.get_cars_by_owner(owner)

        data = {
            'email': owner.email,
            'name': owner.name,
            'cars': [{
                'type': car.car_type.name,
                'color': car.car_color.name,
                'uuid': car.uuid
            } for car in list_of_cars]
        }
        return data

    @staticmethod
    @blueprint.get('/get_all')
    @doc.validate(
        resp=Response(HTTP_200=GetListOfOwners),
        query=OwnerFilter,
        tags=['owner']
    )
    @validate()
    def get_all_owners():
        '''
        Get all registered owners in the system
        '''
        owner_filter: str = request.args.get('sale_opportunity', 'false')
        owner_filter = owner_filter.lower() == 'true'
        owner_repository = OwnerRepository()
        owners = owner_repository.get_all_owners(owner_filter)
        updated_owners = []
        for owner in owners:
            if len(owner.cars) == 0:
                situation = 'Sale Oportunitty'
            elif len(owner.cars) < 3:
                situation = 'Partially full'
            else:
                situation = 'Fully'
            data = ListAboutUser(
                email=owner.email,
                name=owner.name,
                cars=len(owner.cars),
                situation=situation
            )
            updated_owners.append(data)
        return GetListOfOwners(owners=updated_owners)
    
    @staticmethod
    @blueprint.delete('/delete/<owner_email>')
    @doc.validate(
        resp=Response(
            HTTP_200=DeleteOwnerResponse,
            HTTP_404=DeleteOwnerResponse
        ),
        query=OwnerFilter,
        tags=['owner']
    )
    @validate()
    def delete_owner(owner_email: str):
        '''
        Delete an owner registered in the system
        '''
        owner_repository = OwnerRepository()
        try:
            owner_repository.delete_owner(owner_email)
        except OwnerNotFound:
            http_exception(404, {'status': 'Owner not found'})
        return {
            'status': True
        }
    
    @staticmethod
    @blueprint.get('/count')
    @doc.validate(
        resp=Response(HTTP_200=GetOwnersCount),
        tags=['owner']
    )
    @validate()
    def get_owner_count():
        '''
        Get the value of owners registered in the system 
        '''
        owner_repository = OwnerRepository()
        owners = owner_repository.get_owner_count()
        return {
            'owner_count': owners
        }