from enum import Enum
from typing import List

from pydantic import BaseModel


class SubType(Enum):
    ASAP = "ASAP"
    Daily = "Daily"
    Weekly = "Weekly"


class Timer(BaseModel):
    day: str
    hour: str
    minutes: str
    am_pm: str


class UserReg(BaseModel):
    email: str
    subscription_type: SubType
    at_what_time: List[Timer] = []
    categories: List[str] = []
