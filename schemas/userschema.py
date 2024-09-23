from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    phone: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
