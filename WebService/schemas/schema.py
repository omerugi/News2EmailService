from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class SubType(Enum):
    ASAP = "ASAP"
    Daily = "Daily"
    Weekly = "Weekly"


class Timer(BaseModel):
    day: Optional[str]
    time: str


class UserReg(BaseModel):
    email: str
    subscription_type: SubType
    at_what_time: Optional[Timer] = []
    categories: List[str] = []
