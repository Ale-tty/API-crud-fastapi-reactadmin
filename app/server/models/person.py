from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class PersonSchema(BaseModel):
    email: EmailStr = Field(...)
    name: str = Field(...)


class UpdatePersonModel(BaseModel):
    email: Optional[EmailStr]
    name: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "email": "alice@x.com",
                "name": "Alice",
            }
        }


class UserSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Abdulazeez Abdulazeez Adeshina",
                "email": "abdulazeez@x.com",
                "password": "weakpassword"
            }
        }


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "abdulazeez@x.com",
                "password": "weakpassword"
            }
        }


def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
