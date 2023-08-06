from datetime import datetime, date

from .base import CpObject


class Person(CpObject):
    first_name: str = None
    last_name: str = None
    middle_name: str = None
    birth: date = None
    address: str = None
    street: str = None
    city: str = None
    country: str = None
    phone: str = None
    post_code: str = None

    class Config:
        json_encoders = {date: lambda v: datetime.strptime(v, "%Y-%m-%d").date()}
