from pydantic import BaseModel

class UserAuth(BaseModel):
    username: str
    password: str

class AccessToken(BaseModel):
    access_token: str

class ErrorAuth(BaseModel):
    status: str