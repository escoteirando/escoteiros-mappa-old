""" Login: POST /api/escotistas/login
{
    "type": "LOGIN_REQUEST",
    "username": "username",
    "password": "password"
}
"""
from datetime import datetime

from base_model.base_model import BaseModel


class LoginModel(BaseModel):

    id: str
    ttl: int
    created: datetime
    userId: int
