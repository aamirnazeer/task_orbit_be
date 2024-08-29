from pydantic import BaseModel, Field
from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    user = "user"
    guest = "guest"


class CreateNewUser(BaseModel):
    email: str = Field(min_length=5)
    username: str = Field(min_length=3)
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)
    password: str = Field(min_length=3)
    role: UserRole
    phone_number: str = Field(min_length=5)

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "john@doe.com",
                "username": "john",
                "first_name": "john",
                "last_name": "doe",
                "password": "password123",
                "role": "user",
                "phone_number": "999999999"
            }
        }
    }


class SignIn(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=3)

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "john",
                "password": "password123",
            }
        }
    }

