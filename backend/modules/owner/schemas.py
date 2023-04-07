from typing import List
from pydantic import BaseModel

class RegisterOwnerRequest(BaseModel):
    name: str
    email: str

class RegisterOwnerResponse(BaseModel):
    status: bool | str

class GetOwnersCount(BaseModel):
    owner_count: int

class RegisterCarRequest(BaseModel):
    car_type: str
    car_color: str
    owner_email: str

class GetCarTypesResponse(BaseModel):
    car_types: List[str]

class GetCarColorsResponse(BaseModel):
    car_colors: List[str]

class GetCarsCount(BaseModel):
    car_count: int

class AboutCar(BaseModel):
    color: str
    type: str

class GetAboutOwner(BaseModel):
    email: str
    name: str

class AboutOwnerWithCars(GetAboutOwner):
    cars: List[AboutCar]

class ListAboutUser(GetAboutOwner):
    cars: int
    situation: str

class GetListOfOwners(BaseModel):
    owners: List[ListAboutUser]

class OwnerFilter(BaseModel):
    sale_opportunity: bool = False

class DeleteOwnerResponse(BaseModel):
    status: bool