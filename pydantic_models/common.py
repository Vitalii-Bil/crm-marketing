import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, constr
import enum


class ResponseBaseModel(BaseModel):
    class Config:
        orm_mode = True


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class OrderStatus(enum.Enum):
    Free = "Free"
    InWork = "In work"
    Delivery = "Delivery"
    Done = "Done"


class OrderStatusUpdate(enum.Enum):
    InWork = "In work"
    Delivery = "Delivery"
    Done = "Done"


class SphereType(enum.Enum):
    Shop = "Shop"
    Social = "Social"
    Government = "Government"
    Artist = "Artist"
    Business = "Business"


class OrderCreateRequest(BaseModel):
    order_name: str
    order_details: str
    sphere_type: SphereType


class ClientRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    birthday: datetime.date
    phone_number: Optional[
        constr(
            strip_whitespace=True,
            regex=r"^(\+)[1-9][0-9\-\(\)\.]{11,15}$",
        )
    ]
    city: str
    address: str


class LeaveCommentRequest(BaseModel):
    comment_details: str


class ManagerRegistrationRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    birthday: datetime.date
    phone_number: Optional[
        constr(
            strip_whitespace=True,
            regex=r"^(\+)[1-9][0-9\-\(\)\.]{11,15}$",
        )
    ]


class OrderUpdateRequest(BaseModel):
    order_name: Optional[str]
    order_details: Optional[str]
    sphere_type: Optional[SphereType]
