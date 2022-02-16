from typing import List, Optional
from pydantic import BaseModel


class Timer(BaseModel):
    day: Optional[str]
    time: str


class UserReg(BaseModel):
    email: str
    subscription_type: str
    at_what_time: Optional[Timer] = []
    categories: List[str] = []
