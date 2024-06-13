from pydantic import BaseModel
from datetime import date


class BaseRole(BaseModel):
    name: str
    description: str


class GetRole(BaseRole):
    id: int


class BaseUser(BaseModel):
    name: str
    surname: str
    patronymics: str
    email: str
    phone: str
    data_bith: date | None = None
    passport_series: str | None = None
    passport_number: str | None = None


class GetUser(BaseUser):
    id: int
    trace_id: str
    role: GetRole
    role_id: int


class PostUser(BaseUser):
    password: str
    id_role: int = 0
