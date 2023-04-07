from datetime import datetime
from typing import List, Optional
from sqlmodel import SQLModel, Field

class UserModel(SQLModel, table=True):

    __tablename__ = 'users'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(nullable=False)
    password: str = Field(nullable=False)

    member_at: datetime = Field(default_factory=lambda: datetime.utcnow())
