from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class SubType(Enum):
    ASAP = "ASAP"
    Daily = "Daily"
    Weekly = "Weekly"


class AmPm(Enum):
    am = "am"
    pm = "pm"


class Timer(BaseModel):
    day: Optional[str]
    hour: str
    minutes: str
    am_pm: AmPm


class UserReg(BaseModel):
    email: str
    subscription_type: SubType
    at_what_time: Optional[List[Timer]] = []
    categories: List[str] = []
