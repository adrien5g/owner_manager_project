from typing import List
import uuid
from typing import Optional
from datetime import datetime

from sqlmodel import Relationship, SQLModel, Field

class OwnerModel(SQLModel, table=True):

    __tablename__ = 'owners'

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True)
    registered_at: datetime = Field(default_factory=lambda: datetime.utcnow())

    cars: List['CarModel'] = Relationship(back_populates='car_owner')

class CarModel(SQLModel, table=True):
    
    __tablename__ = 'cars'

    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), unique=True)
    color: int = Field(foreign_key='car_colors.id')
    type: int = Field(foreign_key='car_type.id')
    owner: int = Field(foreign_key='owners.id', nullable=False)

    car_owner: OwnerModel = Relationship(back_populates='cars')
    car_color: 'CarColorModel' = Relationship(back_populates='cars')
    car_type : 'CarTypeModel' = Relationship(back_populates='cars')

class CarColorModel(SQLModel, table=True):
    
    __tablename__ = 'car_colors'

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    cars: List[CarModel] = Relationship(back_populates='car_color')

class CarTypeModel(SQLModel, table=True):
    
    __tablename__ = 'car_type'

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    cars: List[CarModel] = Relationship(back_populates='car_type')
